# NextReach – Web Chatbot Contact Agent

**Prepared by:** Berke B.  
**Project Type:** Internship Technical Assessment (6-Hour Challenge)

---

# Overview

NextReach is a B2B SaaS company that provides analytics dashboards for mid-sized ecommerce businesses.

The goal of this project is to replace the traditional **"Contact Sales"** form with a conversational chatbot experience that feels more welcoming while collecting enough information for the sales team to take action.

Instead of simply storing contact requests, the application also evaluates lead quality, generates a recommended next action, and provides an internal dashboard for reviewing incoming leads.

---

# Live Demo

(Add Render deployment link here)

---

# Screens

- Landing Page
- Product Tour
- Chatbot Contact Flow
- Admin Dashboard

---

# Features

## Landing Page

- Modern SaaS landing page
- Contact Sales CTA
- Product Tour page
- Social proof section
- Testimonials
- Pricing cards
- Fully responsive layout

---

## Conversational Chatbot

Instead of displaying a cold contact form, visitors interact with a guided chatbot.

The chatbot collects information naturally and helps users who are unsure what they want to ask.

Features:

- Friendly conversational flow
- Progress indicator
- Typing animation
- Required & optional questions
- Skip support for optional fields
- Client-side validation
- Email validation

---

## Lead Qualification

Each contact request is automatically scored.

Collected information includes:

- Business need
- Company
- Website
- Ecommerce platform
- Urgency
- Budget
- Contact person
- Job title
- Business email
- Preferred follow-up method

The application generates:

- Lead Score
- Lead Quality (High / Medium / Low)
- Summary
- Next Best Action

---

## Admin Dashboard

The internal dashboard allows the sales team to quickly review incoming leads.

Dashboard includes:

- Total Leads
- High Quality Leads
- New Leads
- Lead Quality Distribution
- Search
- Lead cards
- Contact information
- Need summary
- Budget
- Platform
- Status updates
- Internal notes
- CSV Export

---

## Spam Protection

Basic protection was implemented for the MVP:

- Honeypot field
- Simple rate limiting
- Blocked phrase detection
- Minimum text validation

---

# Technology Stack

Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite

Frontend

- HTML
- CSS
- Vanilla JavaScript
- Jinja2 Templates

Deployment

- Render

---

# Why These Technologies?

FastAPI provides a modern Python backend that is lightweight, easy to understand, and fast to develop within a short timeframe.

SQLite keeps the MVP self-contained without requiring any external database setup.

Vanilla JavaScript was intentionally chosen to keep the project lightweight while demonstrating understanding of frontend fundamentals without relying on heavy frameworks.

---

# Chatbot Flow

The chatbot asks the visitor:

1. What do you need help with?
2. Company name
3. Company website
4. Ecommerce platform
5. Urgency
6. Budget
7. Contact person's name
8. Role
9. Business email
10. Preferred follow-up method

Required fields:

- Need
- Company
- Name
- Email
- Urgency

Optional fields:

- Website
- Platform
- Budget
- Role
- Preferred contact

---

# When Does The Chatbot Stop?

The chatbot stops after collecting enough information for the sales team to confidently answer four questions:

- Who contacted us?
- Which company are they from?
- Why are they reaching out?
- How should we contact them?

The objective is qualification rather than collecting unnecessary information.

---

# Chatbot Personality

The chatbot was intentionally designed to feel:

- Professional
- Friendly
- Efficient
- Business-oriented

Since NextReach is a B2B SaaS company, the chatbot avoids sounding overly playful while still reducing the cold feeling of a traditional contact form.

---

# Lead Quality Logic

Lead quality is calculated using a deterministic scoring system.

Signals considered:

- Company information
- Email validity
- Business need clarity
- Website
- Job role
- Budget
- Ecommerce platform
- Urgency

Output:

- High
- Medium
- Low

Additionally, the system generates a **Next Best Action** recommendation for the sales team.

Examples:

High + Urgent

> Contact today. High buying intent.

Medium

> Follow up to clarify budget and timeline.

Low

> Review manually before prioritizing.

---

# Admin Dashboard Decisions

The admin dashboard was designed around one simple question:

> "Which leads should the sales team contact first?"

Instead of only listing submissions, the dashboard highlights:

- Lead Quality
- Priority
- Summary
- Next Best Action
- Current Status
- Internal Notes

This reduces the amount of manual review required.

---

# Handling Missing Answers

Some visitors may not wish to answer every question.

Optional fields support the keyword:

```
skip
```

Required information cannot be skipped because the sales team would otherwise receive incomplete requests.

---

# Handling Spam

For this MVP the following measures were implemented:

- Honeypot field
- Rate limiting
- Blocked keywords
- Minimum message length

Given additional development time, I would implement:

- Google reCAPTCHA
- IP reputation checking
- Email verification
- AI spam classification

---

# Future Improvements

Given more development time I would implement:

- Authentication
- PostgreSQL
- Docker
- Unit tests
- CRM integration (HubSpot, Salesforce)
- Email notifications
- Slack notifications
- AI-powered intent classification
- Semantic lead scoring
- Conversation analytics
- Chatbot drop-off analytics
- Dark Mode
- Multi-language support
- Accessibility improvements

---

# Running Locally

Create a virtual environment:

```bash
python -m venv venv
```

Activate:

macOS/Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
uvicorn app.main:app --reload
```

Landing Page

```
http://127.0.0.1:8000
```

Admin Dashboard

```
http://127.0.0.1:8000/admin
```

(Optional)

Generate demo leads:

```bash
python -m app.seed
```

---

# Project Structure

```
nextreach-chatbot-agent/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── schemas.py
│   ├── lead_scoring.py
│   └── seed.py
│
├── templates/
│
├── static/
│
├── requirements.txt
│
└── README.md
```

---

# PRD Interpretation

Several product decisions were intentionally left open in the original PRD.

My interpretation was to build a **Lead Qualification Assistant** rather than a general AI chatbot.

The chatbot's primary objective is not to answer every possible question.

Instead, it should:

- reduce friction,
- guide uncertain visitors,
- collect actionable business context,
- and help the sales team prioritize incoming requests.

This interpretation aligns with the original business problem described in the PRD.

---

# Time Spent

Approximately **6 hours**, following the assessment requirements.