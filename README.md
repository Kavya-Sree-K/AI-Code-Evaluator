# 💻 AI Code Evaluator

## 📌 Project Overview

AI Code Evaluator is an intelligent coding assistant that generates, executes, evaluates, and analyzes programming solutions in real time.

The platform allows users to enter coding-related questions, automatically generate executable code, run the generated program with dynamic inputs, and receive AI-powered evaluation with quality scores, feedback, and improvement suggestions.

The system provides a complete coding workflow within a single interface, making it useful for students, developers, interview preparation, and programming practice.

---

## 🎯 Objectives

* Generate executable code from coding queries.
* Support multiple programming-related questions.
* Execute generated code in real time.
* Accept dynamic user inputs during execution.
* Analyze code quality automatically.
* Provide feedback and suggestions for improvement.
* Maintain history of previously asked questions.

---

## ✨ Features

### 🚀 Code Generation

Generate complete executable code from user coding questions.

### ▶ Real-Time Code Execution

Execute generated programs directly from the application.

### ⌨ Dynamic Input Support

Automatically detects input statements and creates input fields for users.

### 📊 AI Code Evaluation

Evaluates generated code and provides a quality score.

### 📝 Smart Feedback

Provides detailed feedback regarding:

* Code correctness
* Readability
* Logic
* Structure
* Best practices

### 🚀 Improvement Suggestions

Suggests improvements when code quality can be enhanced.

### 🕘 Previous Question History

Stores previously asked questions permanently using JSON storage.

### 🗑 Delete History

Allows users to remove unwanted questions from history.

### ➕ New Query Mode

Users can switch between history view and new query mode.

### 🌐 Multi-Language Query Support

Supports coding-related questions from different programming domains.

### ⚡ Modern User Interface

Built with Streamlit and custom styling for an interactive experience.

---

## 🛠 Tech Stack

### Frontend

* Python
* Streamlit
* HTML
* CSS

### Backend

* Python

### AI Models

* Ollama (Local LLM)
* Gemini AI

### Storage

* JSON File Storage (`history.json`)

### Libraries Used

* streamlit
* requests
* google-generativeai
* python-dotenv
* tempfile
* subprocess
* json
* re
* os
* time

---

## 📂 Project Structure

```text
AI-Code-Evaluator/
│
├── app.py
├── view.py
├── history.json
├── .env
├── requirements.txt
├── README.md
│
└── __pycache__/
```

### app.py

Responsible for:

* Code generation
* AI evaluation
* Prompt engineering
* Communication with AI models

### view.py

Responsible for:

* User Interface
* Dynamic Inputs
* Code Execution
* History Management
* Displaying Results

### history.json

Stores:

* Previous Questions
* Generated Code
* Scores
* Feedback
* Suggestions

---

## ⚙ Requirements

### Software Requirements

* Python 3.10+
* VS Code
* Ollama
* Git

### AI Requirements

Install Ollama and pull a model:

```bash
ollama pull llama3
```

### Gemini API Key

Create a `.env` file:

```env
Google_Api_Key=YOUR_GEMINI_API_KEY
```

---

## 📦 Installation

### Clone Repository

```bash
git clone https://github.com/Kavya-Sree-K/AI-Code-Evaluator.git
```

### Move into Project Folder

```bash
cd AI-Code-Evaluator
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶ Running the Application

### Step 1

Start Ollama:

```bash
ollama serve
```

### Step 2

Run the Streamlit application:

```bash
streamlit run view.py
```

### Step 3

Open browser:

```text
http://localhost:8501
```

---

## 🧑‍💻 User Workflow

### Generate Code

1. Enter coding question.
2. Click Generate Code.
3. View generated solution.

### Execute Code

1. Enter required inputs.
2. Click Run Code.
3. View output.

### Evaluate Code

View:

* Score
* Feedback
* Suggestions

### View History

1. Open sidebar.
2. Select previous question.
3. View previously generated results.

### Delete History

1. Click delete icon beside question.
2. Question is removed permanently.

---

## 📊 Output Generated

The application provides:

* Generated Code
* Program Output
* AI Evaluation Score
* Feedback
* Suggestions

---

## 🚀 Future Enhancements

* Retrieval Augmented Generation (RAG)
* Code Complexity Analysis
* Multi-Model Evaluation
* Code Explanation Module
* PDF Report Generation
* Database Storage
* User Authentication
* Cloud Deployment
* Coding Interview Mode
* Code Comparison Feature

---

## 👥 Contributor
Kavya Sree

## 📜 License

This project is developed for educational and learning purposes.
