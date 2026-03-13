from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Azure Network Inventory API")

# Temporary in-memory database for first version
devices = {}


class Device(BaseModel):
    hostname: str
    ip_address: str
    vendor: str
    model: str
    site: str
    role: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/devices")
def get_devices():
    return list(devices.values())


@app.get("/devices/{hostname}")
def get_device(hostname: str):
    if hostname not in devices:
        raise HTTPException(status_code=404, detail="Device not found")
    return devices[hostname]


@app.post("/devices")
def create_device(device: Device):
    if device.hostname in devices:
        raise HTTPException(status_code=400, detail="Device already exists")
    devices[device.hostname] = device.dict()
    print(devices)
    return {"message": "Device created", "device": devices[device.hostname]}


@app.put("/devices/{hostname}")
def update_device(hostname: str, device: Device):
    if hostname not in devices:
        raise HTTPException(status_code=404, detail="Device not found")
    devices[hostname] = device.dict()
    return {"message": "Device updated", "device": devices[hostname]}


@app.delete("/devices/{hostname}")
def delete_device(hostname: str):
    if hostname not in devices:
        raise HTTPException(status_code=404, detail="Device not found")
    deleted = devices.pop(hostname)
    return {"message": "Device deleted", "device": deleted}

@app.get("/debug")
def debug_devices():
    return devices