from pydantic import BaseModel

class CoordinateData(BaseModel):
    lat: float
    lon: float


