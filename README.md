# 🤖 Groq Streaming Chatbot

A Python-based LLM chatbot built with the **Groq API**, designed to demonstrate core AI Engineering concepts including streaming responses, conversation memory, token management, context summarization, token budgeting, and API cost estimation.

## 🚀 Features

- ⚡ Streaming LLM responses
- 💬 Multi-turn conversation history
- 🔢 Token counting with `tiktoken`
- 🧠 Conversation context management
- 📝 Automatic summarization of older conversations
- 📊 Input and output token tracking
- 💰 API cost estimation
- 🎯 Configurable context and output token budgets
- 🔐 Environment-based API key management

## 🧠 AI Engineering Concepts

This project demonstrates how an LLM application manages:

```text
User Input
     ↓
Conversation History
     ↓
Token Counting
     ↓
Context Management
     ↓
Conversation Summary
     ↓
Groq API
     ↓
Streaming Response
     ↓
Token & Cost Tracking
```

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Groq API | LLM inference |
| `tiktoken` | Token counting |
| `python-dotenv` | Environment variable management |

## 📁 Project Structure

```text
groq-streaming-chatbot/
│
├── chatbot.py          # Main chatbot application
├── token_demo.py       # Tokenization/token counting practice
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── .gitignore          # Files excluded from Git
└── .env                # API key - NOT committed
```

## ⚙️ How It Works

### 1. User Input

The user enters a message through the terminal.

### 2. Conversation History

User and assistant messages are stored so the chatbot can maintain context across multiple turns.

### 3. Token Counting

The application estimates the number of tokens in the conversation using `tiktoken`.

### 4. Context Management

The application monitors the configured context budget.

When the conversation becomes too large, older messages are summarized instead of simply being discarded.

### 5. Streaming

The Groq API response is streamed and displayed token-by-token rather than waiting for the complete response.

### 6. Token & Cost Tracking

After each response, the application displays:

```text
Input tokens
Output tokens
Total tokens
Input cost
Output cost
Total cost
```

## 💰 Cost Estimation

The application estimates API usage using:

```text
Input Cost =
(input tokens / 1,000,000) × input price

Output Cost =
(output tokens / 1,000,000) × output price

Total Cost =
Input Cost + Output Cost
```

The pricing values are configured in `chatbot.py` so they can be updated if the model provider changes its pricing.

## 🖥️ Example

```text
You: What is machine learning?

Assistant: Machine learning is a branch of artificial intelligence
that enables computers to learn patterns from data...

----------------------------------------
Input tokens:  18
Output tokens: 225
Total tokens:  243
----------------------------------------
Input cost:    $0.00000135
Output cost:   $0.00006750
Total cost:    $0.00006885
----------------------------------------
[Stored conversation tokens: 243]
```

## 🔐 Environment Setup

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

**Never commit your `.env` file or expose your API key publicly.**

The `.gitignore` file prevents `.env` from being committed.

## ▶️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/rahul007828/groq-streaming-chatbot.git
```

### 2. Open the project

```bash
cd groq-streaming-chatbot
```

### 3. Create a virtual environment

Windows:

```bash
python -m venv .venv
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure the API key

Create `.env` and add your Groq API key:

```env
GROQ_API_KEY=your_api_key_here
```

### 6. Run the chatbot

```bash
python chatbot.py
```

## 🧪 Example Commands

Start the application:

```bash
python chatbot.py
```

Exit:

```text
exit
```

## 📚 What I Learned

Through this project, I learned the fundamentals of building an LLM-powered application:

- How LLM APIs work
- What tokens are
- How tokenization affects context and cost
- How conversation history is managed
- How context budgets can be implemented
- Why older conversations may need summarization
- How streaming responses work
- How input and output tokens affect API costs
- How to protect API credentials using environment variables

## 🔮 Future Improvements

Planned improvements include:

- Web-based user interface
- Persistent conversation storage
- Better token accounting using provider usage data
- Authentication
- Deployment as a web application
- Production-ready logging and monitoring

## 👨‍💻 Author

**Rahul Dheeraj**

Aspiring AI Engineer focused on:

```text
Python
Machine Learning
Generative AI
LLM Applications
RAG
AI Agents
```

---

⭐ If you find this project useful, feel free to star the repository.
