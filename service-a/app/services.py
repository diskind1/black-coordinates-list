import os
import requests
from schemas import CoordinatesPayload


EXTERNAL_GEOIP_URL = os.getenv("EXTERNAL_GEOIP_URL", "http://ip-api.com/json")


def get_location_from_external(ip: str):
    try:
        response = requests.get(f"{EXTERNAL_GEOIP_URL}/{ip}")

        response.raise_for_status()
        data = response.json()
        if data.get("status") == "fail":
            raise ValueError("Invalid IP or private network")
        return data.get("lat"), data.get("lon")
    except Exception as e:
        print(f"Error fetching IP location: {e}")
        raise e
    


SERVICE_B_URL = os.getenv("SERVICE_B_URL", "http://localhost:8002")

def send_to_storage(data: CoordinatesPayload):
    try:
        endpoint = f"{SERVICE_B_URL}/coordinates"
        response = requests.post(endpoint, json=data.model_dump())
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error sending to Service B: {e}")
        raise e
    

