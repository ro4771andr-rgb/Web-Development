from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SmartHome IoT API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = {
    "homes": [],
    "rooms": [],
    "devices": []
}

class Device(BaseModel):
    id: int
    name: str
    type: str  # sensor, actuator, lighting
    status: str = "offline"
    last_update: datetime

class Room(BaseModel):
    id: int
    name: str
    home_id: int
    devices: List[Device] = []

class Home(BaseModel):
    id: int
    owner: str
    address: str
    rooms: List[Room] = []

class HomeCreate(BaseModel):
    owner: str
    address: str

class RoomCreate(BaseModel):
    name: str

class DeviceCreate(BaseModel):
    name: str
    type: str

def get_next_id(collection: str) -> int:
    items = db[collection]
    return max([item.id for item in items], default=0) + 1


@app.post("/homes", status_code=status.HTTP_201_CREATED, response_model=Home)
def create_home(data: HomeCreate):
    new_home = Home(id=get_next_id("homes"), **data.model_dump())
    db["homes"].append(new_home)
    return new_home

@app.get("/homes", response_model=List[Home])
def get_homes(
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1),
    sortBy: str = Query("owner", regex="^(owner|address)$")
):
    result = sorted(db["homes"], key=lambda x: getattr(x, sortBy))
    start = (page - 1) * limit
    return result[start : start + limit]

@app.post("/homes/{home_id}/rooms", response_model=Room)
def add_room(home_id: int, data: RoomCreate):
    home = next((h for h in db["homes"] if h.id == home_id), None)
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")
    
    new_room = Room(id=get_next_id("rooms"), home_id=home_id, **data.model_dump())
    db["rooms"].append(new_room)
    home.rooms.append(new_room) 
    return new_room

@app.post("/rooms/{room_id}/devices", response_model=Device)
def add_device(room_id: int, data: DeviceCreate):
    room = next((r for r in db["rooms"] if r.id == room_id), None)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    new_device = Device(
        id=get_next_id("devices"),
        last_update=datetime.now(),
        **data.model_dump()
    )
    db["devices"].append(new_device)
    room.devices.append(new_device) 
    return new_device

@app.put("/devices/{device_id}", response_model=Device)
def update_device_status(device_id: int, new_status: str):
    device = next((d for d in db["devices"] if d.id == device_id), None)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    device.status = new_status
    device.last_update = datetime.now()
    return device

@app.delete("/homes/{home_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_home(home_id: int):
    home = next((h for h in db["homes"] if h.id == home_id), None)
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")
    db["homes"].remove(home)
    return