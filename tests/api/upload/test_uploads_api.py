import pytest
import pytest_asyncio

from models.auth_models.token_response import UserResponse
from models.auth_models.user_login import UserLogin


@pytest_asyncio.fixture(scope="class")
async def img_helper(async_client):
    """Diccionario compartido para guardar tokens durante la ejecución de la clase de tests"""
    return {}

@pytest.mark.asyncio
class TestUploadsApi:

    async def test_upload_image_should_return_201(self, async_client, img_helper):
        user_login_model = UserLogin(username="hola2", password="hola")
    
        user_logged = await async_client.post('/api/v1/auth/login', json=user_login_model.model_dump())
        
        assert user_logged.status_code == 200
        
        json_data = user_logged.json()
        user_response_model = UserResponse(**json_data)
        
        pdf_bytes = b'%PDF_Prueba'
        files = {"file": ("test.pdf", pdf_bytes,"application/pdf")}
        
        res = await async_client.post("/api/v1/uploads/save_img", headers={"Authorization": f"Bearer {user_response_model.access_token}"}, files = files)
        
        assert res.status_code == 201
        
        res_data = res.json()
        
        assert isinstance(res_data, str)
        
        img_helper["img"] = res_data
        
    async def test_download_image_should_return_200(self, async_client, img_helper):
        user_login_model = UserLogin(username="hola2", password="hola")
    
        user_logged = await async_client.post('/api/v1/auth/login', json=user_login_model.model_dump())
        
        assert user_logged.status_code == 200
        
        json_data = user_logged.json()
        user_response_model = UserResponse(**json_data)
        
        img_name = img_helper["img"]
        
        print(img_name)
        
        res = await async_client.post("/api/v1/uploads/download", headers={"Authorization": f"Bearer {user_response_model.access_token}"}, json={"img_name": img_name})
        
        print(res.headers["Content-Disposition"])
        
        assert res.status_code == 200
        assert res.headers["Content-Type"] == "application/pdf"
        assert res.headers["Content-Disposition"] == f"attachment; filename={img_name}"

        pdf_bytes = res.content
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        
        
        