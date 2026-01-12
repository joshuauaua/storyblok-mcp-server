
import asyncio
import json
from config import Config
from utils.api import build_management_url, get_management_headers
import httpx

async def fetch_components():
    cfg = Config()
    url = build_management_url("/components")
    headers = get_management_headers()
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            components = data.get("components", [])
            for comp in components:
                if comp.get("name") == "application":
                    print(json.dumps(comp, indent=2))
                    return
            print("Component 'application' not found. Listing all names:")
            for comp in components:
                print(comp.get("name"))
        else:
            print(f"Error: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    asyncio.run(fetch_components())
