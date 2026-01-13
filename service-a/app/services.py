import os
import httpx
import ipaddress

def _is_private_or_reserved(ip: str) -> bool:
    try:
        addr = ipaddress.ip_address(ip)
        return (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_multicast
            or addr.is_reserved
        )
    except ValueError:
        return True



EXTERNAL_GEOIP_URL = os.getenv("EXTERNAL_GEOIP_URL", "http://ip-api.com/json")

async def fetch_coords_for_ip(ip: str) -> tuple[float, float]:
    url = f"{EXTERNAL_GEOIP_URL}/{ip}"

    if _is_private_or_reserved(ip):
        raise ValueError("Private/Local IP is not supported for GeoIP lookup")


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
