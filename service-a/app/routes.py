from fastapi import APIRouter, HTTPException
from schemas import ResolveIpRequest, CoordinatesPayload
from services import get_location_from_external, send_to_storage


router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}



@router.post("/resolve-ip", response_model=CoordinatesPayload)
def resolve_ip(body: ResolveIpRequest):
    try:
        lat, lon = get_location_from_external(body.ip)

        payload = CoordinatesPayload(ip=body.ip, lat=lat, lon=lon)
        send_to_storage(payload)
        print ("aaaaaaaaaaa")
        return payload
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


