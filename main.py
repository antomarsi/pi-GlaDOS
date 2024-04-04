from dotenv import load_dotenv
from glados import Glados
import os
import asyncio
import glob

if __name__ == "__main__":
    del os.environ["NLU_MODEL"]
    del os.environ["MODELS_PATH"]
    load_dotenv()
    nlu_path = os.getenv("NLU_MODEL", None)
    model_folder = os.getenv("MODELS_PATH", None)
    if not nlu_path:
        nlu_files = glob.glob(os.path.join(model_folder, "nlu-*.tar.gz"))
        nlu_files.sort(reverse=True)
        if len(nlu_files) == 0:
            raise Exception("No NLU model found")
        nlu_path = nlu_files[0].split("\\")[-1]

    model_path = os.path.join(model_folder, nlu_path)
    api_key = os.getenv("GEMINI_API_KEY")
    print(f"Initializing... using model: {model_path}")
    glados = Glados(gemini_api_key=api_key, model=model_path, spotify_creds=[
        os.getenv("SPOTIFY_CLIENT_ID"),
        os.getenv("SPOTIFY_CLIENT_SECRET"),
    ])
    print("Loading")
    glados.load()
    print("Running")
    asyncio.run(glados.run())
