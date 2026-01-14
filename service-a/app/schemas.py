from pydantic import BaseModel, Field

class ResolveIpRequest(BaseModel):
    ip: str = Field(..., min_length=7)

class CoordinatesPayload(BaseModel):
    ip: str
    lat: float
    lon: float
