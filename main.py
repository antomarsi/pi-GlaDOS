from dotenv import load_dotenv
from glados import Glados
import os
import asyncio
from gemini import Gemini


if __name__ == "__main__":
    load_dotenv()
    model_path = os.path.join(os.getenv("MODELS_PATH"), os.getenv("NLU_MODEL"))
    api_key = os.getenv("GEMINI_API_KEY")
    print("Initializing")
    glados = Glados(gemini_api_key=api_key, model=model_path)
    print("Loading")
    glados.load()
    print("Running")
    asyncio.run(glados.run())
