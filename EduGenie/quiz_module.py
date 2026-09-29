import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def clean_json_block(text: str) -> str:
    """
    Remove Markdown ```json code fences
    """
    cleaned = re.sub(r"```(?:json)?\n?(.*?)\n?```", r"\1", text, flags=re.DOTALL).strip()
    return cleaned

def generate_quiz(text: str) -> list:
    """
    Generates three multiple-choice questions (MCQs) from a given passage or topic.
    Each contains 4 options and a correct answer.
    """
    current_key = os.getenv("GEMINI_API_KEY")
    if not current_key:
        # Provide sample educational MCQs if key is not yet configured
        return [
            {
                "question": f"What is a primary concept related to '{text}'?",
                "options": [
                    f"Core foundational principles of {text}",
                    "Unrelated astronomical phenomenon",
                    "Random geological structure",
                    "Discontinued mechanical protocol"
                ],
                "answer": f"Core foundational principles of {text}"
            },
            {
                "question": f"How can a learner best practice understanding {text}?",
                "options": [
                    "Through regular hands-on application and study",
                    "By ignoring documentation",
                    "By guessing randomly without review",
                    "None of the above"
                ],
                "answer": "Through regular hands-on application and study"
            },
            {
                "question": f"Which field commonly utilizes knowledge of {text}?",
                "options": [
                    "Academic & practical learning domains",
                    "Antique clock restoration exclusively",
                    "Deep-sea submarine welding only",
                    "Fictional spellcasting"
                ],
                "answer": "Academic & practical learning domains"
            }
        ]

    try:
        genai.configure(api_key=current_key)
        prompt = f"""You are a quiz generator.

From the following passage or topic, create exactly 3 multiple-choice questions. Each question should include:
- A "question" string
- A list of 4 "options" strings
- A correct "answer" string that must exactly match one of the options.

Format your output strictly as **valid JSON** array of objects, like this:
[
  {{
    "question": "What is ...?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Option A"
  }}
]

Passage / Topic:
{text}
"""
        response_text = ""
        for model_name in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.5-flash"]:
            try:
                model = genai.GenerativeModel(model_name=model_name)
                response = model.generate_content(prompt)
                if hasattr(response, "text") and response.text:
                    response_text = response.text.strip()
                    break
            except Exception:
                continue

        if not response_text:
            return [{"question": "No quiz content could be generated.", "options": ["N/A", "N/A", "N/A", "N/A"], "answer": "N/A"}]

        cleaned_text = clean_json_block(response_text)
        
        # Try direct JSON parsing
        try:
            quiz_data = json.loads(cleaned_text)
            if isinstance(quiz_data, list) and len(quiz_data) > 0:
                return quiz_data
        except json.JSONDecodeError:
            # Try extracting JSON array with regex
            json_match = re.search(r"\[\s*\{.*\}\s*\]", response_text, re.DOTALL)
            if json_match:
                quiz_data = json.loads(json_match.group(0))
                return quiz_data

        return [{"question": f"Could not parse quiz output: {cleaned_text[:100]}", "options": ["N/A", "N/A", "N/A", "N/A"], "answer": "N/A"}]

    except Exception as e:
        return [{"question": f"⚠️ Error generating quiz: {str(e)}", "options": ["Error", "Error", "Error", "Error"], "answer": "Error"}]
