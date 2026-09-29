import os
from dotenv import load_dotenv

load_dotenv()

# Attempt to load local HuggingFace LaMini model if transformers/torch are installed
_local_model_loaded = False
explain_tokenizer = None
explain_model = None

try:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    import torch
    
    MODEL_NAME = "MBZUAI/LaMini-Flan-T5-783M"
    # Note: Model will be loaded on demand or cached if available
    try:
        # Check if model files are cached or can be quickly loaded
        explain_tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        explain_model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        _local_model_loaded = True
    except Exception as e:
        # Model download might be in progress or offline; fallback ready
        _local_model_loaded = False
except ImportError:
    _local_model_loaded = False


def explain_topic(topic: str) -> str:
    """
    Explains the concept in a simple and clear way for a school student.
    Uses local LaMini-Flan-T5 model or cloud Gemini model as appropriate.
    """
    global _local_model_loaded, explain_tokenizer, explain_model
    
    # 1. Try local LaMini-Flan-T5 if available
    if _local_model_loaded and explain_tokenizer is not None and explain_model is not None:
        try:
            input_text = f"Explain the concept of '{topic}' in a simple and clear way for a school student."
            inputs = explain_tokenizer(input_text, return_tensors="pt")
            outputs = explain_model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                do_sample=True
            )
            explanation = explain_tokenizer.decode(outputs[0], skip_special_tokens=True)
            return explanation.strip()
        except Exception:
            pass # Fall back to cloud model

    # 2. Fallback to Gemini with educational prompt
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            prompt = f"Explain the concept of '{topic}' in a simple and clear way for a school student in 2-4 concise, easy-to-understand sentences."
            for m in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.5-flash"]:
                try:
                    model = genai.GenerativeModel(model_name=m)
                    resp = model.generate_content(prompt)
                    if hasattr(resp, "text") and resp.text:
                        return resp.text.strip()
                except Exception:
                    continue
        else:
            return f"To get an AI explanation of '{topic}', please configure your GEMINI_API_KEY in the .env file."
    except Exception as e:
        return f"⚠️ Error in Explanation: {str(e)}"
    
    return f"Unable to generate explanation for '{topic}'."
