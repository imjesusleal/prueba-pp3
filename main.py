from dotenv import load_dotenv
from fastapi import FastAPI
from api.auth import router as auth_routher

load_dotenv()

app = FastAPI()

app.include_router(auth_routher)