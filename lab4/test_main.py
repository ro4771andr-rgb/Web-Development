import sys
import os
import pytest
from httpx import ASGITransport, AsyncClient

sys.path.append(os.path.abspath("../lab2"))

try:
    from main import app
except ImportError as e:
    raise e

@pytest.mark.asyncio
async def test_get_homes():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/homes")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_home():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {"owner": "Lab4_Tester", "address": "Test Street 123"}
        response = await ac.post("/homes", json=payload)
    assert response.status_code == 201
    assert response.json()["owner"] == "Lab4_Tester"

@pytest.mark.asyncio
async def test_invalid_home_creation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/homes", json={})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_complex_scenario():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {"owner": "Complex Tester", "address": "Complex Street 456"}
        create_response = await ac.post("/homes", json=payload)
        assert create_response.status_code == 201
        
        created_home = create_response.json()
        home_id = created_home.get("id") 
        assert home_id is not None

        get_response = await ac.get("/homes")
        assert get_response.status_code == 200
        
        all_homes = get_response.json()
        assert any(home.get("id") == home_id for home in all_homes), "New home ID not found in the list"