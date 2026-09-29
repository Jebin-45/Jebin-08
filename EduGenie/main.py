from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from qna import answer_question_with_gemini
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

app = FastAPI(title="EduGenie - AI Learning Assistant", description="Google Gemini Powered Educational Platform")

# Mount static files and templates
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Render main application homepage.
    """
    return templates.TemplateResponse(request=request, name="index.html")


# Q&A - GET & POST API using Gemini
@app.get("/qa")
async def answer_question(question: str = Query(...)):
    if not question or not question.strip():
        return JSONResponse(content={"error": "Please provide a valid question."}, status_code=400)
    answer = answer_question_with_gemini(question)
    return {"answer": answer}


@app.post("/qa")
async def answer_question_post(request: Request):
    data = await request.json()
    question = data.get("question")
    if not question:
        return JSONResponse(content={"error": "Please provide a question."}, status_code=400)
    answer = answer_question_with_gemini(question)
    return {"answer": answer}


# Explanation - POST API
@app.post("/explain")
async def explain_api(request: Request):
    data = await request.json()
    topic = data.get("topic")
    if not topic:
        return JSONResponse(content={"error": "Please provide a topic."}, status_code=400)
    explanation = explain_topic(topic)
    return {"topic": topic, "explanation": explanation}


# Summarization - POST API
@app.post("/summarize")
async def summarize_api(request: Request):
    data = await request.json()
    text = data.get("text")
    if not text:
        return JSONResponse(content={"error": "Please provide text to summarize."}, status_code=400)
    summary = summarize_text(text)
    return {"summary": summary}


# Quiz Generation - POST API
@app.post("/quiz")
async def quiz_api(request: Request):
    data = await request.json()
    text = data.get("text")
    if not text:
        return JSONResponse(content={"error": "Please provide text for quiz."}, status_code=400)
    quiz = generate_quiz(text)
    print("Generated quiz:", quiz) # DEBUG
    return JSONResponse(content={"quiz": quiz})


# Learning Recommendations - GET & POST API
@app.get("/learn/recommendations")
async def learning_recommendation_api(topic: str = Query(...)):
    if not topic or not topic.strip():
        return JSONResponse(content={"error": "Please provide a topic."}, status_code=400)
    recommendation = get_learning_recommendations(topic)
    return {"topic": topic, "recommendation": recommendation}


@app.post("/learn/recommendations")
async def learning_recommendation_post_api(request: Request):
    data = await request.json()
    topic = data.get("topic")
    if not topic:
        return JSONResponse(content={"error": "Please provide a topic."}, status_code=400)
    recommendation = get_learning_recommendations(topic)
    return {"topic": topic, "recommendation": recommendation}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
