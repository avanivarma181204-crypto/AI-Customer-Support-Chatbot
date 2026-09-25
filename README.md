# AI Customer Support Chatbot with Memory

## Project Overview

The **AI Customer Support Chatbot with Memory** is a Python-based customer support application that answers common customer questions and remembers important customer information across conversations.

The chatbot can remember:

- Customer name
- Order ID
- Previous customer issue
- Conversation history

The project uses a JSON knowledge base for customer-support information and a JSON memory file for persistent storage.

> **Technical description:** This implementation uses rule-based natural-language/keyword matching with persistent JSON memory. It does not require a paid API or external AI service.

---

## Problem Statement

Customers frequently ask support teams repetitive questions about orders, delivery, returns, refunds, payments, and accounts.

A chatbot can provide immediate answers to common questions and reduce repetitive support work.

A normal chatbot may forget information when the program is restarted. This project addresses that problem by storing important customer information and conversation history in a persistent JSON memory file.

---

## Objectives

1. Build a Python customer-support chatbot.
2. Answer frequently asked customer-support questions automatically.
3. Store customer information during conversations.
4. Remember information after restarting the program.
5. Maintain conversation history.
6. Provide a simple command-line interface.
7. Build the project without requiring a paid API.

---

## Features

### 1. Customer Name Memory

The chatbot can recognize:

```text
My name is Avani
````

It stores the customer's name and can later answer:

```text
What is my name?
```

---

### 2. Order ID Memory

The chatbot recognizes order IDs such as:

```text
My order ID is ORD12345
```

It stores the order ID and can later answer:

```text
What is my order ID?
```

---

### 3. Persistent Memory

Customer information is stored in:

```text
memory.json
```

Because the information is stored in a file, the chatbot can remember information even after the program is closed and restarted.

---

### 4. Conversation History

Every conversation is stored with:

* Timestamp
* User message
* Chatbot response

---

### 5. Customer Support Topics

The chatbot can handle:

* Orders
* Order status
* Delivery
* Late delivery
* Returns
* Refunds
* Payments
* Account issues
* Password assistance
* Customer support information
* Order cancellation

---

## Technologies Used

| Technology          | Purpose                              |
| ------------------- | ------------------------------------ |
| Python              | Main programming language            |
| JSON                | Knowledge base and persistent memory |
| Regular Expressions | Extract customer names and order IDs |
| Rule-Based NLP      | Identify customer intent             |
| VS Code             | Development environment              |

The project uses Python's built-in libraries and does not require a paid API.

---

## Project Structure

```text
AI-Customer-Support-Chatbot/
│
├── app.py
├── knowledge_base.json
├── memory.json
├── .gitignore
└── README.md
```

### app.py

Contains the main chatbot logic.

It is responsible for:

* Reading user input
* Detecting customer intent
* Extracting customer information
* Generating responses
* Saving conversations

### knowledge_base.json

Contains predefined customer-support information about:

* Orders
* Delivery
* Returns
* Refunds
* Payments
* Accounts
* Support

### memory.json

Stores:

* Customer name
* Order ID
* Previous issue
* Conversation history

### README.md

Contains the project documentation and instructions.

---

## How the Chatbot Works

```text
User enters a message
        ↓
Message is processed
        ↓
Customer information is detected
        ↓
Customer intent is identified
        ↓
Relevant knowledge-base information is selected
        ↓
Response is generated
        ↓
Conversation is saved to memory.json
        ↓
Chatbot waits for the next message
```

---

## Memory Mechanism

The memory feature is one of the main components of the project.

For example:

```text
You: My name is Avani

Bot: Nice to meet you, Avani!
```

The name is stored in `memory.json`.

Then:

```text
You: My order ID is ORD12345

Bot: Thank you. I have saved your order ID as ORD12345.
```

The order ID is also stored.

Later:

```text
You: What do you remember?

Bot: Here is what I remember:
Customer name: Avani
Order ID: ORD12345
Previous issue: Delivery issue
```

After closing and restarting:

```text
Welcome back, Avani!
```

The chatbot can also answer:

```text
You: What is my order ID?

Bot: Yes. Your saved order ID is ORD12345.
```

This demonstrates persistent memory across sessions.

---

## Example Conversation

```text
AI CUSTOMER SUPPORT CHATBOT WITH MEMORY

Welcome to AI Customer Support Chatbot!

You: My name is Avani

Bot: Nice to meet you, Avani! I will remember your name
during our conversations.

You: My order ID is ORD12345

Bot: Thank you. I have saved your order ID as ORD12345.
How can I help you with this order?

You: How long does delivery take?

Bot: Standard delivery usually takes 3 to 5 business days.

You: How long does a refund take?

Bot: Refunds are generally processed within 5 to 7 business
days after a return is approved.

You: What do you remember?

Bot: Here is what I remember:
Customer name: Avani
Order ID: ORD12345
Previous issue: Refund issue
```

---

## How to Run the Project

### Step 1: Open the project folder

Open the project in VS Code.

### Step 2: Open the terminal

Select:

```text
Terminal → New Terminal
```

### Step 3: Navigate to the project

```bash
cd ~/Desktop/AI-Customer-Support-Chatbot
```

### Step 4: Run the chatbot

```bash
python3 app.py
```

### Step 5: Start chatting

Example:

```text
My name is Avani
```

```text
My order ID is ORD12345
```

```text
What do you remember?
```

### Step 6: Exit

```text
bye
```

The conversation memory is saved automatically.

---

## API and Database

This version does **not** require:

* OpenAI API
* Paid API keys
* External databases

The project uses:

* `knowledge_base.json` for support information
* `memory.json` for persistent customer memory

This makes the project easy to run locally.

---

## Advantages

* Simple and easy to use
* No paid API required
* Persistent customer memory
* Fast responses
* Easy to modify
* Beginner-friendly
* Separate knowledge base
* Conversation history

---

## Limitations

The current version uses predefined rules and keyword/phrase matching.

Therefore:

* It may not understand completely new questions.
* It does not use a large language model.
* It does not connect to a real order-management system.
* Order status is based on predefined responses.
* It currently runs through the command line.

---

## Future Enhancements

The project can be extended by adding:

1. A web-based interface using Flask or FastAPI.
2. A database such as MySQL.
3. Real-time order tracking.
4. User authentication.
5. Multilingual support.
6. Sentiment analysis.
7. Machine-learning intent classification.
8. Integration with a free or local language model.
9. Voice-based customer support.
10. An admin dashboard.

---

## Learning Outcomes

This project demonstrates:

* Python programming
* Functions
* Conditional statements
* Loops
* Regular expressions
* JSON file handling
* Data persistence
* Rule-based natural-language processing
* Exception handling
* Conversation management
* Basic chatbot architecture

---

## Conclusion

The **AI Customer Support Chatbot with Memory** demonstrates how a Python application can automate common customer-support interactions while maintaining persistent customer information.

The chatbot can remember important information such as customer name and order ID, answer common support questions, and store conversation history for future sessions.

The project provides a foundation that can later be extended into a web-based, database-driven, multilingual, or AI-powered customer-support system.
