import asyncio
import httpx
from config import Config
from utils.api import build_management_url, get_management_headers

# List of tags to sync
ALL_TAGS = [
  "Agents", "AI", "Analytics", "API Integration", "API Security", "API Testing", "Audio", "Audio Playback", "Authentication", "Automotive", "AWS", "Banking", "Barcode", "Browser Automation", "Business Application", "Business Intelligence", "Business Management", "Charts", "Chat", "Checkout", "Cloud", "Code Review", "Configuration", "Contact Management", "Content Management", "Content Type", "Conversational AI", "Course Management", "CRM", "Cron", "Cron Expression", "CRUD", "CSV", "Customer Management", "Dashboard", "Data Encoding", "Data Export", "Data Format", "Data Generation", "Data Import", "Data Management", "Data Tracking", "Data Transformation", "Data Visualization", "Data Warehouse", "Database", "Database Explorer", "Date Calculation", "Date/Time", "DateTime", "DateTime Handling", "Dealership", "Demo", "Developer Tools", "Diff", "Distance Metrics", "DNS", "Document Generation", "DOM", "Domain Name System", "DTO", "E-commerce", "Education", "Enum", "Excel", "Expression Trees", "Fake Data", "File Comparison", "File Processing", "File Types", "Financial", "Flags", "Formatting", "Formula Analysis", "Formula Parsing", "Function Calling", "Fuzzy Matching", "Fuzzy Search", "Getting Started", "GitHub", "Graphics", "Handlebars", "Headless Chrome", "HTML Generation", "HTML Parsing", "HTTP", "Humanization", "IANA", "IBAN", "ID Generation", "Image Generation", "Image Manipulation", "Image Processing", "Image-to-Text", "ImageMagick", "Import/Export", "Infrastructure", "Integration", "Inventory Management", "JSON", "JSON Conversion", "JWT", "Language Processing", "Lead Management", "Lead Tracking", "LINQ", "Liquid", "LLM", "Local AI", "Mapping", "Markdown", "Measurements", "Media", "Member Access", "Microsoft Agent Framework", "MIME Type", "Mock Data", "Multi-Agent", "Natural Language Processing", "Network", "Network Tools", "Object Mapping", "OCR", "Office Documents", "Ollama", "OpenAI", "Optimization", "Parser Combinator", "Parsing", "Payment Processing", "PDF", "PDF Generation", "Performance", "Physical Quantities", "Product Management", "QR Code", "Query", "Reflection", "Report Generation", "REST API", "Runtime", "Sales", "Sales Analytics", "Scheduling", "Screenshot", "Search", "Security", "Semantic Kernel", "Serialization", "Shopify", "Snowflake", "Sortable ID", "Sound Processing", "Spreadsheet", "SQL", "Starter", "Statistics", "Streaming", "String Formatting", "String Matching", "String Similarity", "Stripe", "Task Scheduling", "Template", "Template Engine", "Templating", "Testing", "Text Analysis", "Text Comparison", "Text Generation", "Text Matching", "Text Processing", "Text Recognition", "Text Search", "Text Transformation", "Time Conversion", "Time Manipulation", "Timezone", "Token Management", "Tool Invocation", "Tools", "Type System", "ULID", "Unique Identifier", "Unit Conversion", "Units", "Validation", "vCard", "Venture Capital", "Version Control", "Web Scraping", "Web Services", "Windows Timezone", "Word Documents", "XPath", "YAML", "Zero Allocation"
]

async def sync_tags():
    cfg = Config()
    headers = get_management_headers()
    
    # 1. Get existing tags
    url = build_management_url("/tags")
    existing_tags = set()
    
    async with httpx.AsyncClient() as client:
        print("Fetching existing tags...")
        resp = await client.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            for tag in data.get("tags", []):
                existing_tags.add(tag["name"])
        
        print(f"Found {len(existing_tags)} existing tags.")
        
        # 2. Add missing tags
        tags_to_add = [t for t in ALL_TAGS if t not in existing_tags]
        print(f"Adding {len(tags_to_add)} new tags...")
        
        for i, tag_name in enumerate(tags_to_add):
            payload = {"tag": {"name": tag_name}}
            post_url = build_management_url("/tags/")
            
            retries = 3
            while retries > 0:
                resp = await client.post(post_url, json=payload, headers=headers)
                
                if resp.status_code in [200, 201]:
                    print(f"[{i+1}/{len(tags_to_add)}] Created: {tag_name}")
                    break
                elif resp.status_code == 422:
                    # Already exists
                    # print(f"[{i+1}/{len(tags_to_add)}] Exists: {tag_name}")
                    break
                elif resp.status_code == 429:
                    print(f"Rate limited for {tag_name}. Waiting...")
                    await asyncio.sleep(2) # Wait 2s
                    retries -= 1
                else:
                    print(f"Error creating {tag_name}: {resp.status_code} {resp.text}")
                    break
            
            # Rate limiting or nice handling
            await asyncio.sleep(0.25)

if __name__ == "__main__":
    asyncio.run(sync_tags())
