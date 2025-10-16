from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth

app = FastAPI(
    title="Medify API",
    description="API de Medify aplicación para tomar citas médicas y reseñar profesionales de la salud",
    version="1.0.0"
)

#health-->pruebas unitarias
@app.get("/health", tags=["Health Check"])
def healt_check():
    return{"status": "ok"}

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Medify API is running", "version": "1.0.0"}