
import asyncio
import json
from config import Config
from utils.api import build_management_url, get_management_headers
import httpx

async def debug_tags():
    cfg = Config()
    story_id = 132183463987532 # Hello2U ID
    url = build_management_url(f"/stories/{story_id}")
    headers = get_management_headers()
    
    # 1. Fetch current story to get current content
    print("Fetching story...")
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"Error fetching: {resp.status_code} {resp.text}")
            return
            
        data = resp.json()
        story = data["story"]
        current_content = story["content"]
        
        print("Current Tags in content:", current_content.get("Tags"))
        
        # 2. Update with a test tag
        print("Updating story with Tags: ['mcp-test-tag']...")
        current_content["Tags"] = ["mcp-test-tag"]
        
        payload = {"story": {"content": current_content}}
        
        resp = await client.put(url, headers=headers, json=payload)
        if resp.status_code != 200:
            print(f"Error updating: {resp.status_code} {resp.text}")
            return

        print("Update successful.")

        # 3. Fetch again to verify
        print("Verifying update...")
        resp = await client.get(url, headers=headers)
        data = resp.json()
        new_content = data["story"]["content"]
        print("New Tags in content:", new_content.get("Tags"))

if __name__ == "__main__":
    asyncio.run(debug_tags())
