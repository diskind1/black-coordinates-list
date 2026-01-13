from fastapi import APIRouter, HTTPException
from app.schemas import ResolveIpRequest, CoordinatesPayload

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/resolve-ip", response_model=CoordinatesPayload)
async def resolve_ip(body: ResolveIpRequest):
    raise HTTPException(status_code=501, detail="Not implemented yet")
