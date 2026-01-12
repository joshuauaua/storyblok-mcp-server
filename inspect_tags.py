import asyncio
import json
from config import Config
from utils.api import build_management_url, get_management_headers
import httpx

async def inspect_tags():
    cfg = Config()
    url = build_management_url("/tags")
    headers = get_management_headers()
    
    async with httpx.AsyncClient() as client:
        print(f"Fetching tags from {url}...")
        resp = await client.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            tags = data.get("tags", [])
            print(f"Found {len(tags)} tags:")
            for tag in tags:
                print(f" - {tag.get('name')} (Count: {tag.get('taggings_count')})")
        else:
            print(f"Error: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    asyncio.run(inspect_tags())
