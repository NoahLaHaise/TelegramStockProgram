from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

def chat_message(message: str, include_search: bool = True, pro_model: bool = False) -> str:
    client = genai.Client()

    if include_search:
        grounding_tool = types.Tool(google_search=types.GoogleSearch())
    
    if pro_model:
        model = "gemini-3.1-pro-preview"
    else:
        model = "gemini-3.1-flash-lite-preview"

    config = types.GenerateContentConfig(tools=[grounding_tool] if include_search else [],
                                         thinking_config=types.ThinkingConfig(thinking_level="low"),
                                         #systems_instructions =""
                                         )

    response = client.models.generate_content(
               model=model, 
               contents=message,
               config = config,
            )   
    
    return response.text
