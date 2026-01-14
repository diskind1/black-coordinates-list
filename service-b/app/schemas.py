from pydantic import BaseModel
from typing import Optional

class CoordinateData(BaseModel):
    ip: Optional[str] = None
    lat: float
    lon: float

