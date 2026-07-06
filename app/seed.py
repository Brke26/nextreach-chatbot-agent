from app.database import Base, engine, SessionLocal
from app.models import Lead

Base.metadata.create_all(bind=engine)

db = SessionLocal()

demo_leads = [
    Lead(
        name="Sarah Collins",
        email="sarah@urbanbasket.com",
        role="Head of Ecommerce",
        company="Urban Basket",
        website="https://urbanbasket.example",
        need="We want to understand why our checkout conversion dropped after our last campaign and need better product-level analytics.",
        ecommerce_platform="Shopify Plus",
        urgency="ASAP / this week",
        budget="$1000-$2500 monthly",
        preferred_contact="Meeting link",
        lead_score=95,
        lead_quality="High",
        summary="Urban Basket contacted NextReach about checkout conversion analytics. Urgency: ASAP / this week. Budget: $1000-$2500 monthly.",
        next_best_action="Contact today. This looks like a high-intent lead with urgent timing.",
        status="New",
    ),
    Lead(
        name="Michael Tan",
        email="michael@northlinegoods.com",
        role="Founder",
        company="Northline Goods",
        website="https://northlinegoods.example",
        need="We are comparing analytics tools and want to know whether NextReach can replace our current manual reports.",
        ecommerce_platform="WooCommerce",
        urgency="This month",
        budget="Not sure",
        preferred_contact="Email",
        lead_score=68,
        lead_quality="Medium",
        summary="Northline Goods contacted NextReach about replacing manual ecommerce reports. Urgency: This month. Budget: not provided.",
        next_best_action="Follow up with a qualification question. Clarify budget, company size, and timeline.",
        status="Contacted",
    ),
    Lead(
        name="Alex Rivera",
        email="alex@example.com",
        role=None,
        company="Small Store",
        website=None,
        need="Just checking pricing.",
        ecommerce_platform=None,
        urgency="Just exploring",
        budget=None,
        preferred_contact="Email",
        lead_score=35,
        lead_quality="Low",
        summary="Small Store contacted NextReach about pricing. Urgency: Just exploring. Budget: not provided.",
        next_best_action="Review manually. The request is low-context or missing key buying signals.",
        status="New",
    ),
]

if db.query(Lead).count() == 0:
    db.add_all(demo_leads)
    db.commit()
    print("Demo leads created.")
else:
    print("Database already has leads. No demo data added.")

db.close()