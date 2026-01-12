import asyncio
import json
import httpx
from config import Config
from utils.api import build_management_url, get_management_headers

async def debug_story_update():
    cfg = Config()
    
    # 1. Fetch a story (assuming one exists)
    stories_url = build_management_url("/stories")
    headers = get_management_headers()
    
    story_id = None
    story_data = None
    
    async with httpx.AsyncClient() as client:
        print("Fetching stories...")
        resp = await client.get(stories_url, headers=headers)
        if resp.status_code == 200:
            stories = resp.json().get("stories", [])
            for s in stories:
                if s["name"] == "App Manager": # Try to target a specific one if possible, or just first
                     story_id = s["id"]
                     story_data = s
                     break
            if not story_id and stories:
                story_id = stories[0]["id"]
                story_data = stories[0]
        
        if not story_id:
            print("No stories found.")
            return

        print(f"Targeting story: {story_data['name']} (ID: {story_id})")
        
        # 2. Update Content Tags
        print("Initial Content:", json.dumps(story_data.get("content", {}).get("Tags"), indent=2))
        
        content = story_data.get("content", {})
        new_tags = ["AI", "Analytics"] # Valid tags from our list
        content["Tags"] = new_tags
        
        payload = {"story": {"content": content}}
        update_url = build_management_url(f"/stories/{story_id}")
        
        print(f"Updating content.Tags to: {new_tags}")
        resp = await client.put(update_url, json=payload, headers=headers)
        
        if resp.status_code in [200, 201]:
            updated_story = resp.json().get("story", {})
            updated_tags = updated_story.get("content", {}).get("Tags")
            print("Update success.")
            print("Updated Content Tags:", json.dumps(updated_tags, indent=2))
            
            if updated_tags == new_tags:
                print("VERIFICATION SUCCESS: Tags persisted correctly.")
            else:
                print("VERIFICATION FAILED: persisted tags match input?")
        else:
             print(f"Update failed: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    asyncio.run(debug_story_update())
