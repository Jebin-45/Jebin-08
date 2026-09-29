import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def answer_question_with_gemini(question: str) -> str:
    """
    Answers general knowledge and academic questions using Google Gemini.
    """
    try:
        current_key = os.getenv("GEMINI_API_KEY")
        if not current_key:
            return "Please configure your GEMINI_API_KEY in the .env file to enable live AI question answering."
        
        genai.configure(api_key=current_key)
        
        # Try primary model
        model_names = ["gemini-1.5-flash", "gemini-1.5-pro", "models/gemini-1.5-pro", "gemini-2.5-flash"]
        last_error = None
        for name in model_names:
            try:
                model = genai.GenerativeModel(model_name=name)
                response = model.generate_content(question)
                if hasattr(response, "text") and response.text:
                    return response.text.strip()
                elif hasattr(response, "parts") and response.parts:
                    return response.parts[0].text.strip()
            except Exception as e:
                last_error = e
                continue
                
        if last_error:
            raise last_error
        return "No answer could be generated."
    except Exception as e:
        return f"⚠️ Error in QnA: {str(e)}"
