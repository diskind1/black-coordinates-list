from pydantic import BaseModel, Field

class CoordinateData(BaseModel):
    ip: str = Field(..., min_length=7)
    lat: float
    lon: float
