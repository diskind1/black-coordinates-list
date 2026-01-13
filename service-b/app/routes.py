from typing import List
from fastapi import APIRouter, HTTPException 
from schemas import CoordinateData
from storage import save_coordinate, get_all_coordinates

router = APIRouter()

@router.post("/coordinates")
def store_coordinates(data: CoordinateData):
    try:
        save_coordinate(data)
        return {"message": "Coordinates stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/coordinates", response_model=List[CoordinateData])
def list_coordinates():
    try:
        return get_all_coordinates()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
