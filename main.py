from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from errors.ierror_interface import IError 

from api.auth.auth import auth_router
from api.profiles.medicos import router as profiles_router
from api.profiles.pacientes import router as pacientes_router
from api.uploads.upload import router as upload_router

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
    
    @app.exception_handler(IError)
    async def ierror_exception_handler(request: Request, exc: IError):
        return JSONResponse(
        status_code=exc.http_code,
        content={"detail": exc.msg}
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True
    )

    # Routers
    app.include_router(upload_router.router, prefix="/api/v1")
    app.include_router(auth_router.router, prefix="/api/v1")
    app.include_router(profiles_router.router, prefix="/api/v1")
    app.include_router(pacientes_router.router, prefix="/api/v1")

    
except IError as ex:
    raise Exception(status_code=ex.http_code,detail= f"{ex.msg}")