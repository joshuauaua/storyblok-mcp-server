
import asyncio
import json
from config import Config
from utils.api import build_management_url, get_management_headers, _handle_response
import httpx

async def inspect_datasources():
    cfg = Config()
    url = build_management_url("/datasources")
    headers = get_management_headers()
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            # print(json.dumps(data, indent=2))
            for ds in data.get("datasources", []):
                print(f"ID: {ds['id']}, Name: {ds['name']}, Slug: {ds['slug']}")
                
                # Fetch entries for each
                entries_url = build_management_url(f"/datasource_entries?datasource_id={ds['id']}")
                entries_resp = await client.get(entries_url, headers=headers)
                if entries_resp.status_code == 200:
                    entries = entries_resp.json().get("datasource_entries", [])
                    print("  Entries:")
                    for e in entries:
                        print(f"    - {e['name']} ({e['value']})")
        else:
            print(f"Error: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    asyncio.run(inspect_datasources())
