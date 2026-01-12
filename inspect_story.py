
import asyncio
import json
from config import Config
from utils.api import build_management_url, get_management_headers
import httpx

async def fetch_story():
    cfg = Config()
    # Use the ID found in previous step
    story_id = 132183463987532
    url = build_management_url(f"/stories/{story_id}")
    headers = get_management_headers()
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            story = data.get("story", {})
            print(json.dumps(story, indent=2))
        else:
            print(f"Error: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    asyncio.run(fetch_story())
