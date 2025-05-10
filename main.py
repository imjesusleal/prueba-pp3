from fastapi import FastAPI
from api.electricidad import router as elec_router

app = FastAPI()

app.include_router(elec_router)

