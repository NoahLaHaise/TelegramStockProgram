from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import time
from Prompts.System_Prompts import Telegram_Prompt

load_dotenv()


class GeminiAPI:
    def __init__(self):
        self.client = genai.Client()

    def chat_message(self, message: str, include_search: bool = True, pro_model: bool = False) -> str:
        #self.client = genai.Client()

        if include_search:
            grounding_tool = types.Tool(google_search=types.GoogleSearch())
        
        if pro_model:
            model = "gemini-3.1-pro-preview"
        else:
            model = "gemini-3.1-flash-lite-preview"

        config = types.GenerateContentConfig(tools=[grounding_tool] if include_search else [],
                                            thinking_config=types.ThinkingConfig(thinking_level="low"),
                                            system_instruction = Telegram_Prompt)
                                            

        response = self.client.models.generate_content(
                model=model, 
                contents=message,
                config = config,
                )   
        
        return response.text

    def deep_research(self, research_query: str):
        #client = genai.Client()

        interaction = self.client.interactions.create(
            input=research_query,
            agent='deep-research-pro-preview-12-2025',
            background=True
        )

        print(f"Research started: {interaction.id}")

        while True:
            interaction = self.client.interactions.get(interaction.id)
            if interaction.status == "completed":
                print(interaction.outputs[-1].text)
                break
            elif interaction.status == "failed":
                print(f"Research failed: {interaction.error}")
                break
            time.sleep(10)

