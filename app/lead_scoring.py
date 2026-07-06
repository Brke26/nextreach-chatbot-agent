from app.schemas import LeadCreate


def calculate_lead_score(data: LeadCreate) -> tuple[int, str, str, str]:
    score = 0

    if data.company:
        score += 15

    if data.email:
        score += 15

    if data.need and len(data.need.strip()) >= 40:
        score += 20
    elif data.need:
        score += 10

    if data.website:
        score += 10

    if data.role:
        score += 10

    urgency = data.urgency.lower()

    if any(word in urgency for word in ["asap", "urgent", "immediately", "this week", "today"]):
        score += 20
        urgency_level = "urgent"
    elif any(word in urgency for word in ["month", "soon", "quarter"]):
        score += 12
        urgency_level = "medium"
    else:
        score += 5
        urgency_level = "low"

    if data.budget and data.budget.lower() not in ["not sure", "skip", "prefer not to say"]:
        score += 10

    if data.ecommerce_platform:
        score += 5

    if score >= 75:
        quality = "High"
    elif score >= 45:
        quality = "Medium"
    else:
        quality = "Low"

    summary = (
        f"{data.company} contacted NextReach about: {data.need}. "
        f"Urgency: {data.urgency}. "
        f"Budget: {data.budget or 'not provided'}."
    )

    if quality == "High" and urgency_level == "urgent":
        next_best_action = "Contact today. This looks like a high-intent lead with urgent timing."
    elif quality == "High":
        next_best_action = "Prioritize for sales follow-up. Confirm decision process and schedule a demo."
    elif quality == "Medium":
        next_best_action = "Follow up with a qualification question. Clarify budget, company size, and timeline."
    else:
        next_best_action = "Review manually. The request is low-context or missing key buying signals."

    return score, quality, summary, next_best_action