import httpx

from utils.env import get_env_var

_CLOUDFLARE_API_URL = "https://api.cloudflare.com/client/v4/"
_CLOUDFLARE_API_TOKEN = "Bearer {}".format(get_env_var("CLOUDFLARE_API_TOKEN"))
_CLOUDFLARE_API_HEADERS = {
    "Authorization": _CLOUDFLARE_API_TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json",
}

cloudlfare_client = httpx.Client(
    base_url=_CLOUDFLARE_API_URL,
    headers=_CLOUDFLARE_API_HEADERS,
)


def get_dns_records(zone_id: str):
    url = f"zones/{zone_id}/dns_records"
    response = cloudlfare_client.get(url)
    return response.json()


def create_dns_record(zone_id: str, data: dict):
    url = f"zones/{zone_id}/dns_records"
    response = cloudlfare_client.post(url, json=data)
    return response.json()


def get_dns_record_details(zone_id: str, record_id: str):
    url = f"zones/{zone_id}/dns_records/{record_id}"
    response = cloudlfare_client.get(url)
    return response.json()
