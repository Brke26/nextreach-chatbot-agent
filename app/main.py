import csv
import io
import time
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Lead
from app.schemas import LeadCreate, LeadUpdate
from app.lead_scoring import calculate_lead_score

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NextReach Contact Agent",
    description="Landing page chatbot and admin lead management MVP.",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

request_log = {}


def basic_rate_limit(ip: str):
    now = time.time()
    window_seconds = 60
    max_requests = 8

    timestamps = request_log.get(ip, [])
    timestamps = [ts for ts in timestamps if now - ts < window_seconds]

    if len(timestamps) >= max_requests:
        raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")

    timestamps.append(now)
    request_log[ip] = timestamps


def looks_like_spam(data: LeadCreate) -> bool:
    text = f"{data.name} {data.company} {data.need}".lower()
    blocked = ["test test", "asdf", "qwerty", "lorem ipsum", "http://spam", "casino"]
    return any(word in text for word in blocked)


@app.get("/", response_class=HTMLResponse)
def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/product-tour", response_class=HTMLResponse)
def product_tour_page(request: Request):
    return templates.TemplateResponse("product_tour.html", {"request": request})


@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request, db: Session = Depends(get_db)):
    leads = db.query(Lead).order_by(Lead.created_at.desc()).all()
    return templates.TemplateResponse("admin.html", {"request": request, "leads": leads})


@app.post("/api/leads")
def create_lead(data: LeadCreate, request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host if request.client else "unknown"
    basic_rate_limit(client_ip)

    if data.honeypot:
        raise HTTPException(status_code=400, detail="Invalid submission.")

    if looks_like_spam(data):
        raise HTTPException(status_code=400, detail="Submission looks invalid.")

    score, quality, summary, next_best_action = calculate_lead_score(data)

    lead = Lead(
        name=data.name.strip(),
        email=str(data.email).strip(),
        role=data.role,
        company=data.company.strip(),
        website=data.website,
        need=data.need.strip(),
        ecommerce_platform=data.ecommerce_platform,
        urgency=data.urgency,
        budget=data.budget,
        preferred_contact=data.preferred_contact,
        lead_score=score,
        next_best_action=next_best_action,
        lead_quality=quality,
        summary=summary,
    )

    db.add(lead)
    db.commit()
    db.refresh(lead)

    return {
        "message": "Lead created successfully.",
        "lead_id": lead.id,
        "lead_score": lead.lead_score,
        "lead_quality": lead.lead_quality,
        "next_best_action": lead.next_best_action,
        "summary": lead.summary,
    }


@app.patch("/api/leads/{lead_id}")
def update_lead(lead_id: int, data: LeadUpdate, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found.")

    if data.status is not None:
        lead.status = data.status

    if data.internal_notes is not None:
        lead.internal_notes = data.internal_notes

    db.commit()
    db.refresh(lead)

    return {"message": "Lead updated successfully."}


@app.get("/api/leads.csv")
def export_leads_csv(db: Session = Depends(get_db)):
    leads = db.query(Lead).order_by(Lead.created_at.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "id",
        "created_at",
        "name",
        "email",
        "role",
        "company",
        "website",
        "need",
        "platform",
        "urgency",
        "budget",
        "preferred_contact",
        "score",
        "quality",
        "status",
        "summary",
        "internal_notes",
    ])

    for lead in leads:
        writer.writerow([
            lead.id,
            lead.created_at,
            lead.name,
            lead.email,
            lead.role,
            lead.company,
            lead.website,
            lead.need,
            lead.ecommerce_platform,
            lead.urgency,
            lead.budget,
            lead.preferred_contact,
            lead.lead_score,
            lead.lead_quality,
            lead.status,
            lead.summary,
            lead.internal_notes,
        ])

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=nextreach_leads.csv"}
    )