# EduGenie: Google Gemini Powered Learning Assistant 💡✨

EduGenie is a lightweight AI-powered educational assistant that simplifies learning through generative AI. Designed for students of all academic levels, EduGenie enables users to ask questions, understand complex concepts, generate interactive quizzes, receive personalized learning recommendations, and summarize large educational passages.

---

## 🌟 Features & Scenarios

1. **Ask EduGenie a Question (`/qa`)**:
   - Ask general knowledge or academic questions (e.g., *"Which is the largest ocean?"*).
   - Powered by **Google Gemini** for accurate, smart answers.

2. **Concept Explanation (`/explain`)**:
   - Break down complex topics (e.g., *"Photosynthesis"*, *"Quantum Computing"*) into simple, clear explanations suitable for school students.
   - Powered by instruction-tuned AI (`LaMini-Flan-T5` / `Gemini`).

3. **Paragraph Summarization (`/summarize`)**:
   - Distill lengthy texts and articles into concise, easy-to-revise summaries.

4. **Interactive Quiz Generator (`/quiz`)**:
   - Generates 3 Multiple-Choice Questions (MCQs) with 4 options each from any passage or topic.
   - Interactive UI with instant answer checking (`✅ Correct!` / `❌ Incorrect...`).

5. **Personalized Learning Path (`/learn/recommendations`)**:
   - Generates structured, adaptive curricula with Beginner, Intermediate, and Advanced milestones, timelines, and curated resources (books, videos, practice platforms).

---

## 🏗️ Project Architecture

```
EduGenie/
│
├── main.py                  # FastAPI web application & REST routes
├── explanation_module.py    # Concept explanation logic
├── qna.py                   # Question answering with Gemini
├── quiz_module.py           # Quiz generation & JSON parsing logic
├── summary_module.py        # Passage summarization logic
├── learning_path.py         # Adaptive learning recommendations
│
├── templates/
│   └── index.html           # Modern interactive HTML interface
│
├── static/
│   └── style.css            # Responsive, polished styling
│
├── requirements.txt         # Python dependencies
├── .env.example             # Environment template
└── .env                     # API key configuration
```

---

## 🚀 Quickstart Guide

### 1. Configure Gemini API Key
Create or edit your `.env` file and add your Google Gemini API key:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```
> Get a free API key at [Google AI Studio](https://aistudio.google.com/).

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Server
```bash
uvicorn main:app --reload
```

### 4. Access EduGenie
Open your web browser and navigate to:
**[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 📡 REST API Reference

| Endpoint | Method | Parameters / Body | Description |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | — | Renders the web interface |
| `/qa` | `GET` / `POST` | `question` | Answers academic or GK questions |
| `/explain` | `POST` | `{"topic": "..."}` | Provides simplified explanation |
| `/summarize` | `POST` | `{"text": "..."}` | Summarizes long paragraphs |
| `/quiz` | `POST` | `{"text": "..."}` | Generates 3 MCQs in JSON format |
| `/learn/recommendations` | `GET` / `POST` | `topic` | Produces step-by-step learning roadmap |
