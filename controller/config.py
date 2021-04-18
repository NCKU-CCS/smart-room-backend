import os

from dotenv import load_dotenv

load_dotenv()


HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "7000"))
TOKEN = os.getenv("TOKEN").split(",")
AVAILABLE_COMMAND = [f"{temperature}C" for temperature in range(16, 31)]
AVAILABLE_COMMAND.extend(["off"])
