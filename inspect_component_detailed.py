
import asyncio
import json
from config import Config
from utils.api import build_management_url, get_management_headers
import httpx

async def inspect_component():
    cfg = Config()
    comp_id = 121917339533386
    url = build_management_url(f"/components/{comp_id}")
    headers = get_management_headers()
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    asyncio.run(inspect_component())
