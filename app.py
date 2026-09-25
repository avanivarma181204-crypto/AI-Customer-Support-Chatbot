import json
import re
from datetime import datetime


# ============================================================
# FILE NAMES
# ============================================================

KNOWLEDGE_FILE = "knowledge_base.json"
MEMORY_FILE = "memory.json"


# ============================================================
# LOAD JSON FILE
# ============================================================

def load_json(filename, default):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


# ============================================================
# SAVE JSON FILE
# ============================================================

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

knowledge_base = load_json(KNOWLEDGE_FILE, {})


# ============================================================
# DEFAULT MEMORY
# ============================================================

default_memory = {
    "customer_name": "",
    "order_id": "",
    "previous_issue": "",
    "conversation": []
}


# ============================================================
# LOAD MEMORY
# ============================================================

memory = load_json(MEMORY_FILE, default_memory)

memory.setdefault("customer_name", "")
memory.setdefault("order_id", "")
memory.setdefault("previous_issue", "")
memory.setdefault("conversation", [])


# ============================================================
# REMEMBER CUSTOMER NAME
# ============================================================

def remember_customer_name(message):
    patterns = [
        r"\bmy name is\s+([a-zA-Z]+)",
        r"\bi am\s+([a-zA-Z]+)",
        r"\bi'm\s+([a-zA-Z]+)",
        r"\bcall me\s+([a-zA-Z]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)

        if match:
            name = match.group(1)
            memory["customer_name"] = name
            return name

    return None


# ============================================================
# REMEMBER ORDER ID
# ============================================================

def remember_order_id(message):
    message = message.strip()

    # Example:
    # My order ID is ORD12345
    # My order number is ORD12345
    # Order ID: ORD12345

    match = re.search(
        r"\border\s*(?:id|number)\s*(?:is|:)?\s*(ORD[-]?\d+)\b",
        message,
        re.IGNORECASE
    )

    if match:
        order_id = match.group(1).upper()
        memory["order_id"] = order_id
        return order_id

    # Example:
    # ORD12345
    # ORD-12345

    match = re.search(
        r"\bORD[-]?\d+\b",
        message,
        re.IGNORECASE
    )

    if match:
        order_id = match.group(0).upper()
        memory["order_id"] = order_id
        return order_id

    return None


# ============================================================
# DETECT CUSTOMER ISSUE
# ============================================================

def detect_issue(message):
    text = message.lower()

    if any(word in text for word in [
        "refund",
        "money back"
    ]):
        memory["previous_issue"] = "Refund issue"
        return

    if any(word in text for word in [
        "return",
        "send back",
        "exchange"
    ]):
        memory["previous_issue"] = "Return request"
        return

    if any(word in text for word in [
        "payment",
        "upi",
        "debit card",
        "credit card",
        "net banking",
        "money deducted",
        "transaction"
    ]):
        memory["previous_issue"] = "Payment issue"
        return

    if any(phrase in text for phrase in [
        "cancel order",
        "cancel my order",
        "cancel the order",
        "want to cancel"
    ]):
        memory["previous_issue"] = "Order cancellation"
        return

    if any(word in text for word in [
        "password",
        "login",
        "account"
    ]):
        memory["previous_issue"] = "Account issue"
        return

    if any(word in text for word in [
        "delivery",
        "shipping",
        "arrived",
        "delivered",
        "not arrived",
        "not delivered",
        "order is late"
    ]):
        memory["previous_issue"] = "Delivery issue"
        return


# ============================================================
# GENERATE RESPONSE
# ============================================================

def generate_response(message):
    text = message.lower().strip()

    # --------------------------------------------------------
    # SAVE NAME
    # --------------------------------------------------------

    name = remember_customer_name(message)

    if name:
        return (
            f"Nice to meet you, {name}! "
            "I will remember your name during our conversations."
        )

    # --------------------------------------------------------
    # SAVE ORDER ID
    # --------------------------------------------------------

    order_id = remember_order_id(message)

    if order_id:
        return (
            f"Thank you. I have saved your order ID as {order_id}. "
            "How can I help you with this order?"
        )

    # --------------------------------------------------------
    # ASK NAME
    # --------------------------------------------------------

    if any(phrase in text for phrase in [
        "what is my name",
        "what's my name",
        "do you know my name",
        "remember my name"
    ]):
        if memory["customer_name"]:
            return f"Yes. Your name is {memory['customer_name']}."

        return "I don't have your name saved yet."

    # --------------------------------------------------------
    # ASK ORDER ID
    # --------------------------------------------------------

    if any(phrase in text for phrase in [
        "what is my order id",
        "what's my order id",
        "do you know my order id",
        "remember my order id",
        "what is my order number",
        "what's my order number"
    ]):
        if memory["order_id"]:
            return (
                f"Yes. Your saved order ID is "
                f"{memory['order_id']}."
            )

        return "I don't have an order ID saved yet."

    # --------------------------------------------------------
    # ASK MEMORY
    # --------------------------------------------------------

    if any(phrase in text for phrase in [
        "what do you remember",
        "what do you know about me",
        "show my memory",
        "show memory"
    ]):
        customer_name = memory["customer_name"] or "Not provided"
        order_id = memory["order_id"] or "Not provided"
        previous_issue = (
            memory["previous_issue"]
            or "No issue recorded"
        )

        return (
            "Here is what I remember:\n"
            f"Customer name: {customer_name}\n"
            f"Order ID: {order_id}\n"
            f"Previous issue: {previous_issue}"
        )

    # ========================================================
    # REFUND
    # ========================================================

    if any(word in text for word in [
        "refund",
        "money back"
    ]):
        detect_issue(message)

        if any(phrase in text for phrase in [
            "not received",
            "not got",
            "haven't received",
            "have not received",
            "refund not received"
        ]):
            return knowledge_base["refunds"]["not_received"]

        return knowledge_base["refunds"]["time"]

    # ========================================================
    # RETURN
    # ========================================================

    if any(word in text for word in [
        "return",
        "send back",
        "exchange"
    ]):
        detect_issue(message)

        if any(word in text for word in [
            "how",
            "process",
            "start",
            "procedure"
        ]):
            return knowledge_base["returns"]["process"]

        return knowledge_base["returns"]["policy"]

    # ========================================================
    # PAYMENT
    # ========================================================

    if any(word in text for word in [
        "payment",
        "upi",
        "debit card",
        "credit card",
        "net banking"
    ]):
        detect_issue(message)

        if any(word in text for word in [
            "failed",
            "failure",
            "deducted",
            "money deducted"
        ]):
            return knowledge_base["payments"]["failed"]

        return knowledge_base["payments"]["methods"]

    # ========================================================
    # ORDER CANCELLATION
    # ========================================================

    if any(phrase in text for phrase in [
        "cancel order",
        "cancel my order",
        "cancel the order",
        "want to cancel"
    ]):
        detect_issue(message)
        return knowledge_base["orders"]["cancel"]

    # ========================================================
    # LATE OR MISSING DELIVERY
    # ========================================================

    if any(phrase in text for phrase in [
        "late delivery",
        "delivery is late",
        "order is late",
        "not arrived",
        "not delivered",
        "has not arrived",
        "hasn't arrived",
        "not received my order"
    ]):
        detect_issue(message)

        if memory["order_id"]:
            return (
                f"I understand that your order "
                f"{memory['order_id']} has a delivery issue. "
                + knowledge_base["delivery"]["late"]
            )

        return knowledge_base["delivery"]["late"]

    # ========================================================
    # DELIVERY TIME
    # ========================================================

    if any(phrase in text for phrase in [
        "delivery time",
        "shipping time",
        "when will it arrive",
        "when will my order arrive",
        "how long is delivery",
        "how long does delivery take",
        "how many days for delivery",
        "how many days does delivery take",
        "standard delivery"
    ]):
        detect_issue(message)
        return knowledge_base["delivery"]["time"]

    # ========================================================
    # ORDER STATUS
    # ========================================================

    if any(phrase in text for phrase in [
        "order status",
        "track my order",
        "where is my order",
        "track order"
    ]):
        detect_issue(message)

        if memory["order_id"]:
            return (
                f"Your saved order ID is "
                f"{memory['order_id']}. "
                + knowledge_base["orders"]["status"]
            )

        return knowledge_base["orders"]["status"]

    # ========================================================
    # ACCOUNT
    # ========================================================

    if any(word in text for word in [
        "password",
        "login",
        "account",
        "registered email"
    ]):
        detect_issue(message)

        if any(word in text for word in [
            "password",
            "forgot password",
            "reset password"
        ]):
            return knowledge_base["account"]["password"]

        return knowledge_base["account"]["help"]

    # ========================================================
    # SUPPORT
    # ========================================================

    if any(word in text for word in [
        "support",
        "customer care",
        "contact support",
        "working hours",
        "support hours"
    ]):
        if any(word in text for word in [
            "hours",
            "time",
            "open",
            "close"
        ]):
            return knowledge_base["support"]["working_hours"]

        return knowledge_base["support"]["contact"]

    # ========================================================
    # GREETING
    # ========================================================

    if any(phrase in text for phrase in [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]):
        if memory["customer_name"]:
            return (
                f"Hello {memory['customer_name']}! "
                + knowledge_base["greeting"]
            )

        return knowledge_base["greeting"]

    # ========================================================
    # DEFAULT RESPONSE
    # ========================================================

    return (
        "I'm sorry, I didn't fully understand your question. "
        "I can help with orders, delivery, returns, refunds, "
        "payments, account issues and customer support."
    )


# ============================================================
# SAVE CONVERSATION
# ============================================================

def save_conversation(user_message, bot_response):
    conversation_entry = {
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "user": user_message,
        "bot": bot_response
    }

    memory["conversation"].append(
        conversation_entry
    )

    save_json(
        MEMORY_FILE,
        memory
    )


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("=" * 60)
    print("        AI CUSTOMER SUPPORT CHATBOT WITH MEMORY")
    print("=" * 60)

    if memory["customer_name"]:
        print(
            f"\nWelcome back, {memory['customer_name']}!"
        )
    else:
        print(
            "\nWelcome to AI Customer Support Chatbot!"
        )

    print(
        "I can help with orders, delivery, returns, "
        "refunds, payments and account issues."
    )

    print(
        "\nI can also remember your name, "
        "order ID and previous issue."
    )

    print("\nType 'bye' to exit.\n")

    while True:

        user_message = input("You: ").strip()

        if not user_message:
            continue

        # EXIT
        if user_message.lower() in [
            "bye",
            "exit",
            "quit"
        ]:
            save_json(
                MEMORY_FILE,
                memory
            )

            print(
                "\nBot: Thank you for contacting customer "
                "support. Your conversation memory has been saved."
            )

            print("Goodbye!")
            break

        # GENERATE RESPONSE
        bot_response = generate_response(
            user_message
        )

        # DISPLAY RESPONSE
        print(
            f"Bot: {bot_response}\n"
        )

        # SAVE CONVERSATION
        save_conversation(
            user_message,
            bot_response
        )


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":
    main()