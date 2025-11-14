import pytest

from services.profiles.pacientes.commands.add_paciente_cmd import AddPacienteCmd
from services.profiles.pacientes.commands.updt_paciente_cmd import UpdtPacienteCommand
from models.profiles.paciente_profile import PacienteProfile
from models.auth_models.user_login import UserLogin
from models.auth_models.token_response import UserResponse

@pytest.mark.asyncio
class TestPacienteApi:
    
    async def test_create_paciente_should_return_201(self, async_client):
        
        user_login_model = UserLogin(username="hola2", password="hola")
    
        user_logged = await async_client.post('/api/v1/auth/login', json=user_login_model.model_dump())
        
        assert user_logged.status_code == 200
        
        json_data = user_logged.json()
        user_response_model = UserResponse(**json_data)
        
        paciente: AddPacienteCmd = AddPacienteCmd(id_user=2, documento_identificativo=123456,nombre="jesus", apellido="leal")
        
        res = await async_client.post("/api/v1/profiles/pacientes/create", headers={"Authorization": f"Bearer {user_response_model.access_token}"},json=paciente.model_dump())
        
        assert res.status_code == 201
        
         
    async def test_get_paciente_should_return_200(self, async_client):
        
        user_login_model = UserLogin(username="hola2", password="hola")
    
        user_logged = await async_client.post('/api/v1/auth/login', json=user_login_model.model_dump())
        
        assert user_logged.status_code == 200
        
        json_data = user_logged.json()
        user_response_model: UserResponse = UserResponse(**json_data)
        
        
        res = await async_client.get("/api/v1/profiles/pacientes/get", 
                                      headers={"Authorization": f"Bearer {user_response_model.access_token}"},
                                      params={"user_id":user_response_model.id_user})
        
        assert res.status_code == 200
        
        json_data = res.json()
        paciente_profile_model = PacienteProfile(**json_data)
        
        assert paciente_profile_model.id_user != None
        assert isinstance(paciente_profile_model.id_user, int)
        assert paciente_profile_model.id_user == 2
        assert paciente_profile_model.id_paciente != None
        assert isinstance(paciente_profile_model.id_paciente, int)
        
    async def test_update_paciente_should_return_201(self, async_client):
        
        user_login_model = UserLogin(username="hola2", password="hola")
    
        user_logged = await async_client.post('/api/v1/auth/login', json=user_login_model.model_dump())
        
        assert user_logged.status_code == 200
        
        json_data = user_logged.json()
        user_response_model: UserResponse = UserResponse(**json_data)
        
        cmd = UpdtPacienteCommand(nombre="jesus2", apellido="leal2")
        
        res = await async_client.post("/api/v1/profiles/pacientes/update", 
                                      headers={"Authorization": f"Bearer {user_response_model.access_token}"},
                                      json=cmd.model_dump())
        
        assert res.status_code == 201
    
        