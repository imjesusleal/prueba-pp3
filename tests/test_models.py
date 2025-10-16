import pytest
import asyncio
from db import db
from models.medify_models import Users, UserRoles, Medicos, Turnos

@pytest.mark.asyncio
async def test_models_connection():# solo verifica que los modelos se importen y conecten correctamente
    try: 
        async with db.session() as session:
            print("Modelos cargados correctamente")
            print(f"Conexión a DB establecida")

        print(f"Tabla Users: {Users.__tablename__}")
        print(f"Campos Users: {list(Users.__fields__.keys())}")

    except Exception as e:
        print(f"Error en modelos: {e}")

asyncio.run(test_models_connection())

def test_models_creation_validates():
    usuario = Users(
        id_user = 1,
        username = "Fulano",
        email = "fulano@example.com",
        user_rol = 1
    )

    assert usuario.username == "Fulano"
    assert usuario.email == "fulano@example.com"
    assert usuario.user_rol == 1

def test_modelo_campos_opcionales():
    """Verifica que campos opcionales funcionen correctamente"""
    # Puede crearse sin campos opcionales
    usuario = Users()
    assert usuario.username is None
    assert usuario.email is None

def test_models_validation_pydantic():

    with pytest.raises(Exception):
        Users(
            username="Test",
            email="email.com"  # Email inválido
        ).model_validate({"email": "invalido"})

    with pytest.raises(Exception):
        Users(username = "a" * 101) #test para username con mas de 100 caracteres(revisar tabla db)
