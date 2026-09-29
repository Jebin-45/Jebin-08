import os
import traceback
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def get_learning_recommendations(topic: str) -> str:
    """
    Generates a personalized, structured learning path with beginner, intermediate,
    and advanced levels, timelines, key topics, and curated resources.
    """
    prompt = f"""You are an AI tutor. The student wants to learn about: {topic}.
Suggest a structured and adaptive learning path including key topics, order of learning, and resources (books, videos, tutorials, practice platforms). Include beginner, intermediate, and advanced levels if needed.

Structure the response clearly with sections:
- Overview & Goal
- Beginner Level (Estimated Time, Key Topics, Resources)
- Intermediate Level (Estimated Time, Key Topics, Resources)
- Advanced Level (Estimated Time, Key Topics, Resources)
- Adaptive Learning Tips & Next Steps
"""
    try:
        current_key = os.getenv("GEMINI_API_KEY")
        if not current_key:
            return f"""## Learning Recommendations for "{topic}":

### I. Beginner Level: Building a Foundation (1-2 weeks)
- **Key Topics**: Core concepts, terminology, syntax/fundamentals, basic hands-on examples.
- **Resources**: Online documentation, introductory video courses, interactive tutorials.

### II. Intermediate Level: Practical Applications (2-3 weeks)
- **Key Topics**: Real-world projects, design patterns, integration, problem solving.
- **Resources**: Practice platforms, documentation guides, project walkthroughs.

### III. Advanced Level: Mastery & Optimization (3-4 weeks)
- **Key Topics**: Performance tuning, architecture, security, advanced debugging.
- **Resources**: In-depth books, case studies, community forums.

*(Note: Add your GEMINI_API_KEY in the .env file for dynamic, topic-specific AI curricula!)*"""

        genai.configure(api_key=current_key)
        for model_name in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.5-flash"]:
            try:
                model = genai.GenerativeModel(model_name=model_name)
                response = model.generate_content(prompt)
                print("Gemini raw response:", response)

                if hasattr(response, "text") and response.text:
                    return response.text.strip()
                elif hasattr(response, "parts") and response.parts:
                    return response.parts[0].text.strip()
            except Exception:
                continue

        return "❌ Could not extract content from Gemini response."
    except Exception as e:
        traceback.print_exc()
        return f"❌ Error occurred: {str(e)}"
