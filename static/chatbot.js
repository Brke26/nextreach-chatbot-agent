const chatWidget = document.getElementById("chat-widget");
const openChat = document.getElementById("open-chat");
const closeChat = document.getElementById("close-chat");
const messages = document.getElementById("chat-messages");
const input = document.getElementById("chat-input");
const sendButton = document.getElementById("send-message");
const progressBar = document.getElementById("chat-progress-bar");
const progressText = document.getElementById("chat-progress-text");

const conversation = [
    { key: "need", question: "Hi! 👋 Welcome to NextReach. What brought you here today?", placeholder: "Pricing, demo, analytics problem..." },
    { key: "company", question: "Got it. Which company are you contacting us from?", placeholder: "Company name" },
    { key: "website", question: "What is your company website? You can type skip.", placeholder: "https://example.com" },
    { key: "ecommerce_platform", question: "Which ecommerce platform do you use?", placeholder: "Shopify, WooCommerce, custom..." },
    { key: "urgency", question: "How soon are you looking to solve this?", placeholder: "ASAP, this week, this month, just exploring..." },
    { key: "budget", question: "Do you have a rough monthly budget range? You can type skip.", placeholder: "$500-$1000, not sure, skip..." },
    { key: "name", question: "Who should our sales team contact?", placeholder: "Your name" },
    { key: "role", question: "What is your role? You can type skip.", placeholder: "Founder, Growth Manager..." },
    { key: "email", question: "What is your business email?", placeholder: "you@company.com" },
    { key: "preferred_contact", question: "Best follow-up method?", placeholder: "Email, call, meeting link..." }
];

let currentStep = 0;
let answers = {};

function updateProgress() {
    const percent = Math.round((currentStep / conversation.length) * 100);
    progressBar.style.width = `${percent}%`;
    progressText.textContent = `Step ${Math.min(currentStep + 1, conversation.length)} / ${conversation.length}`;
}

function addMessage(text, sender) {
    const bubble = document.createElement("div");
    bubble.className = `message ${sender}`;
    bubble.textContent = text;
    messages.appendChild(bubble);
    messages.scrollTop = messages.scrollHeight;
}

function showTyping(callback) {
    const typing = document.createElement("div");
    typing.className = "message bot typing";
    typing.textContent = "NextReach Agent is typing...";
    messages.appendChild(typing);
    messages.scrollTop = messages.scrollHeight;

    setTimeout(() => {
        typing.remove();
        callback();
    }, 500);
}

function askCurrentQuestion() {
    updateProgress();
    const step = conversation[currentStep];
    showTyping(() => {
        addMessage(step.question, "bot");
        input.placeholder = step.placeholder;
        input.focus();
    });
}

function normalizeAnswer(value) {
    const trimmed = value.trim();
    if (["skip", "pass", "prefer not to say", "no"].includes(trimmed.toLowerCase())) {
        return "";
    }
    return trimmed;
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function validateStep(key, value) {
    if (["website", "role", "budget", "preferred_contact", "ecommerce_platform"].includes(key)) return true;

    if (!value) {
        addMessage("I need this field to create a useful request for our sales team.", "bot");
        return false;
    }

    if (key === "email" && !isValidEmail(value)) {
        addMessage("Please enter a valid business email address.", "bot");
        return false;
    }

    if (key === "need" && value.length < 10) {
        addMessage("Can you add one more detail so our team understands the request?", "bot");
        return false;
    }

    return true;
}

async function submitLead() {
    progressBar.style.width = "100%";
    progressText.textContent = "Complete";

    showTyping(async () => {
        addMessage("Thanks. I’m creating a sales-ready request now.", "bot");

        const payload = {
            name: answers.name,
            email: answers.email,
            role: answers.role || null,
            company: answers.company,
            website: answers.website || null,
            need: answers.need,
            ecommerce_platform: answers.ecommerce_platform || null,
            urgency: answers.urgency,
            budget: answers.budget || null,
            preferred_contact: answers.preferred_contact || null,
            honeypot: ""
        };

        const response = await fetch("/api/leads", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            addMessage("Something went wrong. Please try again.", "bot");
            return;
        }

        const result = await response.json();

        addMessage(
            `Done. I created a sales-ready request. Lead quality: ${result.lead_quality}. Our team can now prioritize and follow up properly.`,
            "bot"
        );

        input.disabled = true;
        sendButton.disabled = true;
    });
}

function handleSend() {
    const step = conversation[currentStep];
    const rawValue = input.value;
    const value = normalizeAnswer(rawValue);

    if (!rawValue.trim()) return;

    addMessage(rawValue, "user");

    if (!validateStep(step.key, value)) {
        input.value = "";
        return;
    }

    answers[step.key] = value;
    input.value = "";
    currentStep++;

    if (currentStep < conversation.length) {
        askCurrentQuestion();
    } else {
        submitLead();
    }
}

openChat.addEventListener("click", () => {
    chatWidget.classList.remove("hidden");
    if (messages.children.length === 0) askCurrentQuestion();
});

closeChat.addEventListener("click", () => {
    chatWidget.classList.add("hidden");
});

sendButton.addEventListener("click", handleSend);

input.addEventListener("keydown", event => {
    if (event.key === "Enter") handleSend();
});