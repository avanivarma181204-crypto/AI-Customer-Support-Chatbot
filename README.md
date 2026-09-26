# AI Customer Support Chatbot with Memory

## Project Overview

The **AI Customer Support Chatbot with Memory** is a Python-based customer support application designed to automate common customer-support interactions and maintain important customer information across conversations.

The chatbot uses **rule-based natural-language processing**, keyword-based intent detection, a JSON knowledge base, and persistent JSON memory.

It can support multiple customer-service areas including general enquiries, products, services, orders, delivery, returns, refunds, payments, accounts, subscriptions, technical problems, connectivity issues, complaints, feedback, and escalation requests.

The project works locally and does not require a paid external AI API.

---

## Problem Statement

Customer-support teams frequently handle repetitive questions about products, services, orders, payments, accounts, technical problems, and other common issues.

A support chatbot can provide immediate responses to frequently asked questions and reduce repetitive manual work.

Another problem with simple chatbots is that they may forget customer information after the program is closed.

This project addresses both problems by combining automated customer-support responses with a persistent memory system.

---

## Objectives

- Automate common customer-support interactions.
- Identify customer intent using rules and keywords.
- Provide relevant responses from a structured knowledge base.
- Remember important customer information.
- Store customer order or reference IDs.
- Maintain conversation history.
- Preserve information across application restarts.
- Provide a simple local customer-support solution without a paid API.

---

## Key Features

### 1. General Customer Support

The chatbot can respond to common general enquiries and direct customers toward the appropriate support area.

### 2. Product Support

It can handle general questions about:

- Products
- Features
- Specifications
- Availability
- Stock

### 3. Service Support

It can provide information about available services and common service-related enquiries.

### 4. Order Support

The chatbot can assist with:

- Order status
- Order tracking
- Order cancellation
- Reference or order IDs

### 5. Delivery Support

It can respond to delivery-related questions, including delayed or pending deliveries.

### 6. Returns and Refunds

The chatbot can provide general guidance about returns, refund processing, and refund-related questions.

### 7. Payment Support

It can handle common questions involving:

- Payment methods
- Failed payments
- Transaction issues
- Charges
- Payment-related problems

### 8. Account Support

The chatbot can assist with:

- Login problems
- Account issues
- Profile-related questions
- Registered account information

### 9. Password Support

It provides guidance for:

- Forgot password
- Password reset
- Password-related account problems

### 10. Subscription Support

It can respond to questions about:

- Subscriptions
- Plans
- Membership
- Renewals
- Cancellation

### 11. Technical Support

It can provide first-level guidance for:

- Errors
- Software problems
- Installation
- Setup
- Configuration
- Troubleshooting

### 12. Connectivity Support

It can handle common questions involving:

- Internet
- Wi-Fi
- Network
- Connectivity
- Offline issues

### 13. Complaint and Feedback Support

Customers can provide complaints, reviews, suggestions, and feedback.

### 14. Escalation Support

The chatbot can recognize requests to speak with a human representative, supervisor, or support agent.

---

## Persistent Memory

Persistent memory is one of the main features of the project.

The chatbot stores important information in:

```text
memory.json
````

The memory system can store:

* Customer name
* Order/reference ID
* Previous issue
* Conversation history
* Timestamp of conversations

### Example

```text
User: My name is Avani

Bot: Nice to meet you, Avani! I will remember your name.
```

Later:

```text
User: What is my name?

Bot: Your saved name is Avani.
```

The same information remains available after restarting the program.

This demonstrates **persistent memory across sessions**.

---

## Knowledge Base

The chatbot uses:

```text
knowledge_base.json
```

to store customer-support responses.

The knowledge base contains information related to:

* Orders
* Delivery
* Returns
* Refunds
* Payments
* Accounts
* Passwords
* Products
* Services
* Pricing
* Subscriptions
* Technical issues
* Connectivity
* Complaints
* Feedback
* Contact and escalation support

Separating the knowledge base from the main Python program makes the project easier to maintain and expand.

---

## How the Chatbot Works

```text
User enters a message
        ↓
Message processing
        ↓
Customer information extraction
        ↓
Intent detection
        ↓
Knowledge-base lookup
        ↓
Response generation
        ↓
Response displayed to user
        ↓
Conversation saved to memory
```

---

## System Architecture

```text
                 CUSTOMER
                    │
                    ↓
             USER MESSAGE
                    │
                    ↓
          MESSAGE PROCESSING
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
 INFORMATION EXTRACTION   INTENT DETECTION
          │                   │
          └─────────┬─────────┘
                    ↓
             RESPONSE LOGIC
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
 KNOWLEDGE BASE          MEMORY SYSTEM
knowledge_base.json       memory.json
          │                   │
          └─────────┬─────────┘
                    ↓
              CHATBOT RESPONSE
                    │
                    ↓
           CONVERSATION STORAGE
```

---

## Technology Stack

| Technology          | Purpose                              |
| ------------------- | ------------------------------------ |
| Python              | Main programming language            |
| JSON                | Knowledge base and persistent memory |
| Regular Expressions | Customer information extraction      |
| Rule-Based NLP      | Intent detection                     |
| VS Code             | Development environment              |
| Git                 | Version control                      |
| GitHub              | Repository and project submission    |

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

### File Description

**app.py**
Contains the main chatbot logic, intent detection, memory handling, and conversation management.

**knowledge_base.json**
Contains predefined customer-support information and responses.

**memory.json**
Stores customer information and conversation history locally.

**.gitignore**
Prevents private files such as `memory.json` from being uploaded to GitHub.

**README.md**
Contains project documentation, features, setup instructions, and technical information.

---

## Example Conversation

```text
Welcome to AI Customer Support Chatbot!

You: My name is Avani

Bot: Nice to meet you, Avani! I will remember your name
during our conversations.

You: What services do you provide?

Bot: Our customer support service can help with product
and service enquiries, account assistance, transactions,
technical issues, and general customer questions.

You: I have a technical problem

Bot: I can help with common technical issues such as
errors, setup, installation, configuration, software
problems, and troubleshooting.

You: I want to make a complaint

Bot: We are sorry to hear that you experienced a problem.
Please describe your complaint clearly so it can be reviewed.

You: What do you remember?

Bot: Here is what I remember:
Customer name: Avani
Order/reference ID: ...
Previous issue: Complaint
```

---

## How to Run the Project

### Step 1: Open the project

Open the project folder in VS Code.

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

### Step 5: Start interacting

Example:

```text
My name is Avani
```

```text
Tell me about your services
```

```text
I have a technical problem
```

```text
What do you remember?
```

### Step 6: Exit

```text
bye
```

---

## API and Database Information

This project does not require:

* A paid OpenAI API
* A paid external AI service
* A cloud database

The current implementation uses local JSON files for:

```text
knowledge_base.json
memory.json
```

This makes the application easy to run and demonstrate locally.

---

## Advantages

* Multiple customer-support categories
* Persistent customer memory
* Simple architecture
* Easy to maintain
* Fast local responses
* No paid API required
* Expandable knowledge base
* Conversation history
* Beginner-friendly implementation

---

## Limitations

The current implementation uses rule-based intent detection and predefined knowledge-base responses.

Therefore:

* It may not understand every possible wording.
* It cannot provide unrestricted general knowledge like a large language model.
* It does not connect to real company systems.
* Order, payment, and account information is not retrieved from real-time databases.
* The current interface is command-line based.

---

## Future Enhancements

The project can be extended with:

1. Web-based interface using Flask or FastAPI.
2. MySQL or another database.
3. Real-time order and transaction integration.
4. User authentication.
5. Multilingual support.
6. Sentiment analysis.
7. Machine-learning intent classification.
8. Integration with a free or local language model.
9. Voice-based customer support.
10. Admin dashboard and analytics.
11. Live human-agent escalation.
12. Cloud deployment.

---

## Learning Outcomes

This project demonstrates practical knowledge of:

* Python programming
* Functions
* Conditional statements
* Loops
* Regular expressions
* JSON file handling
* Data persistence
* Rule-based NLP
* Intent detection
* Conversation management
* Exception handling
* Git and GitHub
* Project documentation

---

## Conclusion

The **AI Customer Support Chatbot with Memory** demonstrates how Python can be used to automate a broad range of customer-support interactions while maintaining persistent customer information.

The system combines rule-based natural-language processing, a structured knowledge base, and persistent memory to provide a simple and expandable customer-support solution.

The project can be further developed into a web-based, database-driven, multilingual, and AI-powered customer-support platform.

---

## GitHub Repository

Public source code and project documentation:

[https://github.com/avanivarma181204-crypto/AI-Customer-Support-Chatbot](https://github.com/avanivarma181204-crypto/AI-Customer-Support-Chatbot)

