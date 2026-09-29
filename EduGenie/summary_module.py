import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def summarize_text(text: str) -> str:
    """
    Summarizes long paragraphs or educational passages into concise, easy-to-understand versions.
    """
    try:
        current_key = os.getenv("GEMINI_API_KEY")
        if not current_key:
            return "Please configure your GEMINI_API_KEY in the .env file to enable AI summarization."

        genai.configure(api_key=current_key)
        prompt = f"Summarize the following text in simple language:\n\n{text}"

        for model_name in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.5-flash"]:
            try:
                model = genai.GenerativeModel(model_name=model_name)
                response = model.generate_content(prompt)
                if hasattr(response, "text") and response.text:
                    return response.text.strip()
                elif hasattr(response, "parts") and response.parts:
                    return response.parts[0].text.strip()
            except Exception:
                continue

        return "Summary could not be generated."
    except Exception as e:
        return f"⚠️ Error in Summary: {str(e)}"
