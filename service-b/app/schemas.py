from pydantic import BaseModel

class CoordinateData(BaseModel):
    ip: str
    lat: float
    lon: float


