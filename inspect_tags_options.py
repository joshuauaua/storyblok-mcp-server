
import asyncio
import json
from config import Config
from utils.api import build_management_url, get_management_headers
import httpx

async def inspect_tags_options():
    cfg = Config()
    comp_id = 121917339533386
    url = build_management_url(f"/components/{comp_id}")
    headers = get_management_headers()
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            schema = data.get("component", {}).get("schema", {})
            tags_field = schema.get("Tags", {})
            print("Tags Field Schema:")
            print(json.dumps(tags_field, indent=2))
            
            # Check for 'options' list
            options = tags_field.get("options", [])
            print(f"\nOptions found: {len(options)}")
            for opt in options:
                print(f"  Key: '{opt.get('value')}' | Name: '{opt.get('name')}'")
        else:
            print(f"Error: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    asyncio.run(inspect_tags_options())
