import pytest
import pytest_asyncio

from models.auth_models.refresh_model import RefreshModel
from models.auth_models.token_response import UserResponse
from models.auth_models.user_login import UserLogin
from models.auth_models.user_register import UserRegister

@pytest_asyncio.fixture(scope="class")
async def auth_tokens(async_client):
    """Diccionario compartido para guardar tokens durante la ejecución de la clase de tests"""
    return {}

@pytest.mark.usefixtures("seed_roles")
@pytest.mark.asyncio
class TestAuthApi:

    async def test_register_admin_should_return_400(self,async_client):
        
        user_register_model = UserRegister(username="hola", password="hola", email="hola@hola.com", user_rol=1)
    
        res = await async_client.post('/api/v1/auth/register', json=user_register_model.model_dump())
    
        assert res.status_code == 400
    
    @pytest.mark.order(1)
    async def test_register_medico_should_return_201(self, async_client):
        user_register_model = UserRegister(username="hola", password="hola", email="hola@hola.com", user_rol=2)
    
        res = await async_client.post('/api/v1/auth/register', json=user_register_model.model_dump())
    
        assert res.status_code == 201
    
    @pytest.mark.order(2)
    async def test_login_medico_should_return_user_response(self, async_client, auth_tokens):
        user_login_model = UserLogin(username="hola", password="hola")
    
        res = await async_client.post('/api/v1/auth/login', json=user_login_model.model_dump())
  
        assert res.status_code == 200
        
        json_data = res.json()
        user_response_model = UserResponse(**json_data)
        
        assert user_response_model.username == "hola"
        assert isinstance(user_response_model.access_token, str)
        assert isinstance(user_response_model.refresh_token, str) 
        
        # self._medico_tokens: RefreshModel = RefreshModel(refresh_token=user_response_model.refresh_token, id_user=user_response_model.id_user)
        auth_tokens["medico"] = {"refresh_token": user_response_model.refresh_token, "id_user": user_response_model.id_user}

    @pytest.mark.order(3)
    async def test_register_paciente_should_return_201(self, async_client):
        user_register_model = UserRegister(username="hola2", password="hola", email="hola2@hola.com", user_rol=3)
    
        res = await async_client.post('/api/v1/auth/register', json=user_register_model.model_dump())
    
        assert res.status_code == 201
    
    @pytest.mark.order(4)
    async def test_login_paciente_should_return_user_response(self, async_client, auth_tokens):
        user_login_model = UserLogin(username="hola2", password="hola")
    
        res = await async_client.post('/api/v1/auth/login', json=user_login_model.model_dump())
  
        assert res.status_code == 200
        
        json_data = res.json()
        user_response_model = UserResponse(**json_data)
        
        assert user_response_model.username == "hola2"
        assert isinstance(user_response_model.access_token, str)
        assert isinstance(user_response_model.refresh_token, str) 
        
        # self._paciente_tokens: RefreshModel = RefreshModel(refresh_token=user_response_model.refresh_token, id_user=user_response_model.id_user)
        auth_tokens["paciente"] = {"refresh_token": user_response_model.refresh_token, "id_user": user_response_model.id_user}
        
        
    @pytest.mark.order(5)
    async def test_reauthenticate_medico_return_user_response(self, async_client, auth_tokens):   
        token = auth_tokens.get("medico")
        medico_token: RefreshModel = RefreshModel(**token)  
        res = await async_client.post('/api/v1/auth/reauthenticate', json=medico_token.model_dump())
        
        assert res.status_code == 200
        
        json_data = res.json()
        user_response_model = UserResponse(**json_data)
        
        assert user_response_model.username == "hola"
        assert isinstance(user_response_model.access_token, str)
        assert isinstance(user_response_model.refresh_token, str) 
        
    @pytest.mark.order(6)
    async def test_reauthenticate_paciente_return_user_response(self, async_client, auth_tokens):
        token = auth_tokens.get("paciente")  
        paciente_token: RefreshModel = RefreshModel(**token)
        res = await async_client.post('/api/v1/auth/reauthenticate', json=paciente_token.model_dump())
        
        assert res.status_code == 200
        
        json_data = res.json()
        user_response_model = UserResponse(**json_data)
        
        assert user_response_model.username == "hola2"
        assert isinstance(user_response_model.access_token, str)
        assert isinstance(user_response_model.refresh_token, str) 


