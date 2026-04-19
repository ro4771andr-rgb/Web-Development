import sys
import os
import pytest
from httpx import ASGITransport, AsyncClient

sys.path.append(os.path.abspath("../lab2"))

try:
    from main import app
except ImportError as e:
    print(f"\nError: Could not find main.py in ../lab2. Current path: {os.getcwd()}")
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