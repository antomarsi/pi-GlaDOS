
from dotenv import load_dotenv
from glados import Glados


if __name__ == "__main__":
    load_dotenv()
    glados = Glados()
    glados.run()