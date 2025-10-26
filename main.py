from dotenv import load_dotenv
from fastapi import FastAPI
from api.auth import auth_router
from fastapi.middleware.cors import CORSMiddleware

try: 
    
    load_dotenv()

    app = FastAPI(
        title="Medify API",
        description="API de Medify aplicación para tomar citas médicas y reseñar profesionales de la salud",
        version="1.0.0"
    )

    @app.get("/")
    async def root():
        return {"message": "Medify API is running", "version": "1.0.0"}

    #health-->pruebas unitarias
    @app.get("/health", tags=["Health Check"])
    def healt_check():
        return{"status": "ok"}

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(auth_router.router, prefix="/api/v1")
except Exception as ex:
    Exception(f"VOY A LOGEAR EN UN ARCHIVO EN ALGUN MOMENTO, TODAVIA NO PERO SE PINCHO LA APP POR ESTO: {ex.with_traceback()}")