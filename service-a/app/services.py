import os
import ipaddress
import httpx

EXTERNAL_GEOIP_URL = os.getenv("EXTERNAL_GEOIP_URL", "http://ip-api.com/json").rstrip("/")
SERVICE_B_URL = os.getenv("SERVICE_B_URL", "http://service-b:8000").rstrip("/")


def _validate_public_ip(ip: str) -> None:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError as e:
        raise ValueError("Invalid IP address format") from e

    if (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_multicast
        or addr.is_reserved
    ):
        raise ValueError("IP address must be a public (non-private) IP")


async def fetch_coords_for_ip(ip: str) -> tuple[float, float]:
    _validate_public_ip(ip)

    url = f"{EXTERNAL_GEOIP_URL}/{ip}"
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url)

    if r.status_code >= 400:
        raise RuntimeError(f"External GeoIP API returned {r.status_code}: {r.text}")

    data = r.json()

    if isinstance(data, dict) and data.get("status") == "fail":
        msg = data.get("message") or "External GeoIP API failed"
        raise RuntimeError(msg)

    lat = data.get("lat") if isinstance(data, dict) else None
    lon = data.get("lon") if isinstance(data, dict) else None

    if lat is None or lon is None:
        raise RuntimeError("Missing coordinates in external response")

    return float(lat), float(lon)


async def forward_to_service_b(ip: str, lat: float, lon: float) -> None:
    payload = {"ip": ip, "lat": lat, "lon": lon}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(f"{SERVICE_B_URL}/coordinates", json=payload)

    if r.status_code >= 400:
        raise RuntimeError(f"Service B returned {r.status_code}: {r.text}")
