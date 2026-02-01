import google.generativeai as genai
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

async def test():
    model_name = 'gemini-2.0-flash'
    print(f"Testing model: {model_name}")
    try:
        model = genai.GenerativeModel(model_name)
        response = await model.generate_content_async("Hello, are you working?")
        print("Success!")
        print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test())
