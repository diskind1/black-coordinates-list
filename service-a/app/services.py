import os
import httpx

EXTERNAL_GEOIP_URL = os.getenv("EXTERNAL_GEOIP_URL", "http://ip-api.com/json")

async def fetch_coords_for_ip(ip: str) -> tuple[float, float]:
    url = f"{EXTERNAL_GEOIP_URL}/{ip}"

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url)

    if resp.status_code != 200:
        raise RuntimeError(f"External API returned {resp.status_code}")

    data = resp.json()

    if data.get("status") == "fail":
        raise ValueError("Invalid IP or resolution failed")

    lat = data.get("lat")
    lon = data.get("lon")
    if lat is None or lon is None:
        raise RuntimeError("Missing coordinates in external response")

    return float(lat), float(lon)
