import pytest

from services.profiles.medicos.commands.add_medico_command import AddMedicoCommand
from services.profiles.medicos.commands.updt_medico_command import UpdtMedicoCommand
from models.profiles.medifco_profile import MedicoProfile
from models.auth_models.user_login import UserLogin
from models.auth_models.token_response import UserResponse

@pytest.mark.asyncio
class TestMedicosApi:
    
    async def test_create_medico_should_return_201(self, async_client):
        
        user_login_model = UserLogin(username="hola", password="hola")
    
        user_logged = await async_client.post('/api/v1/auth/login', json=user_login_model.model_dump())
        
        assert user_logged.status_code == 200
        
        json_data = user_logged.json()
        user_response_model = UserResponse(**json_data)
        
        medico: AddMedicoCommand = AddMedicoCommand(id_user=1,     especialidad=1,
                                                    documento_identificativo = 1,
                                                    matricula = "prueba",
                                                    telefono = "123412",
                                                    nombre = "jesus",
                                                    apellido = "leal")
        
        res = await async_client.post("/api/v1/profiles/medicos/create", headers={"Authorization": f"Bearer {user_response_model.access_token}"},json=medico.model_dump())
        
        assert res.status_code == 201
        
         
    async def test_get_medico_should_return_200(self, async_client):
        
        user_login_model = UserLogin(username="hola", password="hola")
    
        user_logged = await async_client.post('/api/v1/auth/login', json=user_login_model.model_dump())
        
        assert user_logged.status_code == 200
        
        json_data = user_logged.json()
        user_response_model: UserResponse = UserResponse(**json_data)
        
        
        res = await async_client.get("/api/v1/profiles/medicos/get", 
                                      headers={"Authorization": f"Bearer {user_response_model.access_token}"},
                                      params={"user_id":user_response_model.id_user})
        
        assert res.status_code == 200
        
        json_data = res.json()
        medico_profile_model = MedicoProfile(**json_data)
        
        assert medico_profile_model.id_user != None
        assert isinstance(medico_profile_model.id_user, int)
        assert medico_profile_model.id_user == 1
        assert medico_profile_model.id_medico != None
        assert isinstance(medico_profile_model.id_medico, int)
        
    async def test_update_medico_should_return_201(self, async_client):
        
        user_login_model = UserLogin(username="hola", password="hola")
    
        user_logged = await async_client.post('/api/v1/auth/login', json=user_login_model.model_dump())
        
        assert user_logged.status_code == 200
        
        json_data = user_logged.json()
        user_response_model: UserResponse = UserResponse(**json_data)
        
        cmd = UpdtMedicoCommand(matricula="1234", telefono="9 11 2134 5712")
        
        res = await async_client.post("/api/v1/profiles/medicos/update", 
                                      headers={"Authorization": f"Bearer {user_response_model.access_token}"},
                                      json=cmd.model_dump())
        
        assert res.status_code == 201
    
        