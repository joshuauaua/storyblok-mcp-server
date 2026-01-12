
import asyncio
import json
from config import Config
from utils.api import build_management_url, get_management_headers
import httpx

async def update_tags_schema():
    cfg = Config()
    
    # 1. Fetch Internal Tags
    internal_tags_url = build_management_url("/internal_tags")
    headers = get_management_headers()
    
    internal_tags = []
    async with httpx.AsyncClient() as client:
        print("Fetching internal tags...")
        resp = await client.get(internal_tags_url, headers=headers)
        if resp.status_code == 200:
            internal_tags = resp.json().get("internal_tags", [])
            print(f"Found {len(internal_tags)} internal tags.")
        else:
            print(f"Error fetching tags: {resp.status_code}")
            return

        # Prepare options list from internal tags
        # Storyblok options format: [{"name": "Label", "value": "value"}]
        # We'll use the tag name as both name and value
        new_options = [{"name": t["name"], "value": t["name"]} for t in internal_tags]
        
        # 2. Get current component schema
        comp_id = 121917339533386
        comp_url = build_management_url(f"/components/{comp_id}")
        
        # Fetch existing component to preserve other fields
        resp = await client.get(comp_url, headers=headers)
        if resp.status_code != 200:
             print(f"Error fetching component: {resp.status_code}")
             return

        comp_data = resp.json().get("component", {})
        schema = comp_data.get("schema", {})
        
        if "Tags" not in schema:
            print("Tags field not found in schema!")
            return
            
        # 3. Update the Tags field options
        print("Updating Tags field options...")
        schema["Tags"]["options"] = new_options
        schema["Tags"]["source"] = "self" # Ensure source is explicitly self
        
        # 4. Save component
        payload = {"component": {"schema": schema}}
        resp = await client.put(comp_url, headers=headers, json=payload)
        
        if resp.status_code == 200:
            print("Successfully updated component schema with tag options.")
            print(json.dumps(new_options, indent=2))
        else:
            print(f"Error updating component: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    asyncio.run(update_tags_schema())
