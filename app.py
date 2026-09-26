import json
import re
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_FILE = BASE_DIR / "knowledge_base.json"
MEMORY_FILE = BASE_DIR / "memory.json"


# ---------------------------------------------------------
# FILE HANDLING
# ---------------------------------------------------------

def load_json(file_path, default_data):
    """Load JSON data safely."""
    try:
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data
    except (json.JSONDecodeError, OSError):
        pass

    return default_data


def save_json(file_path, data):
    """Save JSON data safely."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except OSError as error:
        print(f"Unable to save data: {error}")


# ---------------------------------------------------------
# MEMORY
# ---------------------------------------------------------

default_memory = {
    "customer_name": "",
    "order_id": "",
    "previous_issue": "",
    "conversation_history": []
}

memory = load_json(MEMORY_FILE, default_memory)

# Make sure older memory files still work
memory.setdefault("customer_name", "")
memory.setdefault("order_id", "")
memory.setdefault("previous_issue", "")
memory.setdefault("conversation_history", [])


# ---------------------------------------------------------
# KNOWLEDGE BASE
# ---------------------------------------------------------

knowledge_base = load_json(KNOWLEDGE_FILE, {})


# ---------------------------------------------------------
# INFORMATION EXTRACTION
# ---------------------------------------------------------

def extract_customer_name(message):
    """
    Detect names from messages such as:
    My name is Avani
    I am Avani
    I'm Avani
    """
    patterns = [
        r"\bmy name is ([A-Za-z][A-Za-z ]{1,30})\b",
        r"\bi am ([A-Za-z][A-Za-z ]{1,30})\b",
        r"\bi'm ([A-Za-z][A-Za-z ]{1,30})\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            name = match.group(1).strip()

            # Stop common sentence words from becoming part of the name
            stop_words = [
                "and", "but", "because", "from", "with",
                "today", "here", "looking", "having"
            ]

            words = name.split()
            cleaned_words = []

            for word in words:
                if word.lower() in stop_words:
                    break
                cleaned_words.append(word)

            name = " ".join(cleaned_words).strip()

            if name:
                return name.title()

    return None


def extract_order_id(message):
    """
    Detect order/reference IDs such as:
    ORD12345
    ORD-12345
    ORDER12345
    """
    patterns = [
        r"\bORD[- ]?\d{3,}\b",
        r"\bORDER[- ]?\d{3,}\b",
        r"\bREF[- ]?\d{3,}\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            value = match.group(0).upper()
            value = re.sub(r"\s+", "", value)
            return value

    return None


# ---------------------------------------------------------
# INTENT DETECTION
# ---------------------------------------------------------

INTENT_KEYWORDS = {
    "order_status": [
        "order status",
        "where is my order",
        "track my order",
        "track order",
        "order tracking",
        "order update"
    ],

    "order_cancel": [
        "cancel my order",
        "cancel order",
        "want to cancel",
        "cancellation"
    ],

    "delivery": [
        "delivery",
        "arrive",
        "shipping time",
        "how long",
        "delivery time",
        "when will it arrive",
        "late delivery",
        "delayed delivery",
        "shipping delay"
    ],

    "returns": [
        "return",
        "return policy",
        "return product",
        "send back"
    ],

    "refunds": [
        "refund",
        "money back",
        "refund status",
        "refund time"
    ],

    "payments": [
        "payment",
        "payment failed",
        "transaction",
        "money deducted",
        "charged",
        "payment methods",
        "upi",
        "debit card",
        "credit card",
        "net banking"
    ],

    "account": [
        "account",
        "login",
        "log in",
        "sign in",
        "profile",
        "registered email",
        "account help"
    ],

    "password": [
        "password",
        "forgot password",
        "reset password",
        "change password"
    ],

    "products": [
        "product",
        "products",
        "item",
        "items",
        "features",
        "specification",
        "specifications",
        "availability",
        "available",
        "stock"
    ],

    "services": [
        "service",
        "services",
        "what do you offer",
        "what services",
        "your services",
        "offering"
    ],

    "pricing": [
        "price",
        "pricing",
        "cost",
        "charge",
        "charges",
        "fee",
        "fees"
    ],

    "subscription": [
        "subscription",
        "subscribe",
        "renewal",
        "renew",
        "plan",
        "membership"
    ],

    "technical": [
        "technical problem",
        "technical issue",
        "not working",
        "error",
        "bug",
        "problem",
        "troubleshoot",
        "troubleshooting",
        "installation",
        "setup",
        "configuration",
        "software issue"
    ],

    "connectivity": [
        "connection",
        "connectivity",
        "internet",
        "network",
        "wifi",
        "offline"
    ],

    "complaint": [
        "complaint",
        "complain",
        "unhappy",
        "bad experience",
        "poor service",
        "issue with service"
    ],

    "feedback": [
        "feedback",
        "suggestion",
        "suggest",
        "review"
    ],

    "contact": [
        "contact",
        "customer support",
        "support number",
        "phone number",
        "email",
        "working hours",
        "office hours",
        "support hours"
    ],

    "escalation": [
        "escalate",
        "manager",
        "supervisor",
        "human agent",
        "human support",
        "speak to an agent",
        "talk to an agent"
    ]
}


def detect_issue(message):
    """Identify the most likely customer-support intent."""
    text = message.lower().strip()

    # Specific intents first
    priority_order = [
        "password",
        "order_cancel",
        "order_status",
        "refunds",
        "returns",
        "payments",
        "subscription",
        "connectivity",
        "technical",
        "complaint",
        "feedback",
        "escalation",
        "account",
        "delivery",
        "products",
        "services",
        "pricing",
        "contact"
    ]

    for intent in priority_order:
        keywords = INTENT_KEYWORDS.get(intent, [])

        for keyword in keywords:
            if keyword in text:
                return intent

    return "general"


# ---------------------------------------------------------
# RESPONSE GENERATION
# ---------------------------------------------------------

def get_kb_response(intent):
    """Get a response from the JSON knowledge base."""
    intent_data = knowledge_base.get(intent)

    if isinstance(intent_data, str):
        return intent_data

    if isinstance(intent_data, dict):
        # Prefer a general response
        if "response" in intent_data:
            return intent_data["response"]

        # Otherwise combine available text entries
        values = []

        for value in intent_data.values():
            if isinstance(value, str):
                values.append(value)

        if values:
            return " ".join(values)

    return None


def generate_response(user_message):
    """Generate a chatbot response."""
    global memory

    message = user_message.strip()
    lower_message = message.lower()

    # Extract customer name
    name = extract_customer_name(message)

    if name:
        memory["customer_name"] = name
        response = (
            f"Nice to meet you, {name}! "
            "I will remember your name during our conversations."
        )
        memory["previous_issue"] = "Customer introduction"
        return response

    # Extract order ID
    order_id = extract_order_id(message)

    if order_id:
        memory["order_id"] = order_id
        response = (
            f"Thank you. I have saved your order/reference ID as {order_id}. "
            "How can I help you with it?"
        )
        memory["previous_issue"] = "Order/reference ID provided"
        return response

    # Memory questions
    if (
        "what do you remember" in lower_message
        or "what did you remember" in lower_message
        or "show my memory" in lower_message
        or "my details" in lower_message
    ):
        name_text = memory.get("customer_name") or "Not provided"
        order_text = memory.get("order_id") or "Not provided"
        issue_text = memory.get("previous_issue") or "No previous issue recorded"

        return (
            "Here is what I remember:\n"
            f"Customer name: {name_text}\n"
            f"Order/reference ID: {order_text}\n"
            f"Previous issue: {issue_text}"
        )

    # Direct memory questions
    if "what is my order id" in lower_message or "my order id" in lower_message:
        order_id = memory.get("order_id")

        if order_id:
            return f"Yes. Your saved order/reference ID is {order_id}."

        return "I do not have an order/reference ID saved yet."

    if "what is my name" in lower_message:
        name = memory.get("customer_name")

        if name:
            return f"Your saved name is {name}."

        return "I do not have your name saved yet."

    # Greetings
    greetings = [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    if any(lower_message == greeting for greeting in greetings):
        if memory.get("customer_name"):
            return f"Hello, {memory['customer_name']}! How can I help you today?"

        return knowledge_base.get(
            "greeting",
            "Hello! Welcome to our customer support service. How can I help you today?"
        )

    # Detect intent
    intent = detect_issue(message)

    # Save previous issue
    if intent != "general":
        memory["previous_issue"] = intent.replace("_", " ").title()

    # Get response from knowledge base
    response = get_kb_response(intent)

    if response:
        return response

    # Context-aware general response
    if memory.get("customer_name"):
        return (
            f"I'd be happy to help, {memory['customer_name']}. "
            "Please tell me more about your question or issue."
        )

    return (
        "I'd be happy to help. You can ask me about products, services, "
        "orders, delivery, returns, refunds, payments, accounts, "
        "subscriptions, technical issues, complaints, feedback, or general support."
    )


# ---------------------------------------------------------
# MEMORY + CONVERSATION HISTORY
# ---------------------------------------------------------

def save_conversation(user_message, bot_response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    memory["conversation_history"].append({
        "timestamp": timestamp,
        "user": user_message,
        "bot": bot_response
    })

    save_json(MEMORY_FILE, memory)


# ---------------------------------------------------------
# MAIN CHATBOT
# ---------------------------------------------------------

def main():
    print("=" * 60)
    print("       AI CUSTOMER SUPPORT CHATBOT WITH MEMORY")
    print("=" * 60)

    if memory.get("customer_name"):
        print(f"\nWelcome back, {memory['customer_name']}!")
    else:
        print("\nWelcome to AI Customer Support Chatbot!")

    print(
        "\nI can help with general enquiries, products, services, "
        "orders, delivery, returns, refunds, payments, accounts, "
        "subscriptions, technical issues, complaints, feedback and more."
    )

    print("\nType 'bye' to exit.")

    while True:
        try:
            user_message = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBot: Goodbye!")
            save_json(MEMORY_FILE, memory)
            break

        if not user_message:
            print("Bot: Please enter a message so I can help you.")
            continue

        if user_message.lower() in {"bye", "exit", "quit"}:
            response = "Thank you for contacting customer support. Goodbye!"
            print(f"Bot: {response}")
            save_conversation(user_message, response)
            break

        response = generate_response(user_message)
        print(f"Bot: {response}")

        save_conversation(user_message, response)


if __name__ == "__main__":
    main()