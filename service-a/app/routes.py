from fastapi import APIRouter, HTTPException
from app.schemas import ResolveIpRequest, CoordinatesPayload
from app.services import fetch_coords_for_ip

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/resolve-ip", response_model=CoordinatesPayload)
async def resolve_ip(body: ResolveIpRequest):
    try:
        lat, lon = await fetch_coords_for_ip(body.ip)
        return CoordinatesPayload(lat=lat, lon=lon)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"External GeoIP service error: {e}")
