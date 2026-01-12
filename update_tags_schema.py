
import asyncio
import json
from config import Config
from utils.api import build_management_url, get_management_headers
import httpx

async def update_tags_schema():
    cfg = Config()
    
    # 1. Internal Tags / Option List
    ALL_TAGS = [
      "Agents", "AI", "Analytics", "API Integration", "API Security", "API Testing", "Audio", "Audio Playback", "Authentication", "Automotive", "AWS", "Banking", "Barcode", "Browser Automation", "Business Application", "Business Intelligence", "Business Management", "C#", "Charts", "Chat", "Checkout", "Cloud", "Code Review", "Configuration", "Contact Management", "Content Management", "Content Type", "Conversational AI", "Course Management", "CRM", "Cron", "Cron Expression", "CRUD", "CSV", "Customer Management", "Dashboard", "Data Encoding", "Data Export", "Data Format", "Data Generation", "Data Import", "Data Management", "Data Tracking", "Data Transformation", "Data Visualization", "Data Warehouse", "Database", "Database Explorer", "Date Calculation", "Date/Time", "DateTime", "DateTime Handling", "Dealership", "Demo", "Developer Tools", "Diff", "Distance Metrics", "DNS", "Document Generation", "DOM", "Domain Name System", "DTO", "E-commerce", "Education", "Enum", "Excel", "Expression Trees", "Fake Data", "File Comparison", "File Processing", "File Types", "Financial", "Flags", "Formatting", "Formula Analysis", "Formula Parsing", "Function Calling", "Fuzzy Matching", "Fuzzy Search", "Getting Started", "GitHub", "Graphics", "Handlebars", "Headless Chrome", "HTML Generation", "HTML Parsing", "HTTP", "Humanization", "IANA", "IBAN", "ID Generation", "Image Generation", "Image Manipulation", "Image Processing", "Image-to-Text", "ImageMagick", "Import/Export", "Infrastructure", "Integration", "Inventory Management", "JSON", "JSON Conversion", "JWT", "Language Processing", "Lead Management", "Lead Tracking", "LINQ", "Liquid", "LLM", "Local AI", "Mapping", "Markdown", "Measurements", "Media", "Member Access", "Microsoft Agent Framework", "MIME Type", "Mock Data", "Multi-Agent", "Natural Language Processing", "Network", "Network Tools", "Object Mapping", "OCR", "Office Documents", "Ollama", "OpenAI", "Optimization", "Parser Combinator", "Parsing", "Payment Processing", "PDF", "PDF Generation", "Performance", "Physical Quantities", "Product Management", "QR Code", "Query", "Reflection", "Report Generation", "REST API", "Runtime", "Sales", "Sales Analytics", "Scheduling", "Screenshot", "Search", "Security", "Semantic Kernel", "Serialization", "Shopify", "Snowflake", "Sortable ID", "Sound Processing", "Spreadsheet", "SQL", "Starter", "Statistics", "Streaming", "String Formatting", "String Matching", "String Similarity", "Stripe", "Task Scheduling", "Template", "Template Engine", "Templating", "Testing", "Text Analysis", "Text Comparison", "Text Generation", "Text Matching", "Text Processing", "Text Recognition", "Text Search", "Text Transformation", "Time Conversion", "Time Manipulation", "Timezone", "Token Management", "Tool Invocation", "Tools", "Type System", "ULID", "Unique Identifier", "Unit Conversion", "Units", "Validation", "vCard", "Venture Capital", "Version Control", "Web Scraping", "Web Services", "Windows Timezone", "Word Documents", "XPath", "YAML", "Zero Allocation"
    ]

    # Prepare options sorted alaphabetically
    new_options = [{"name": t, "value": t} for t in sorted(ALL_TAGS)]
    
    # 2. Components to Update
    # 121917339533386 = Application
    # 124709109804577 = Gallery
    component_ids = [121917339533386, 124709109804577]
    headers = get_management_headers()

    async with httpx.AsyncClient() as client:
        for comp_id in component_ids:
            print(f"Updating component schema for ID {comp_id}...")
            comp_url = build_management_url(f"/components/{comp_id}")
            
            # Fetch existing component to preserve other fields
            resp = await client.get(comp_url, headers=headers)
            if resp.status_code != 200:
                print(f"Error fetching component {comp_id}: {resp.status_code}")
                continue

            comp_data = resp.json().get("component", {})
            schema = comp_data.get("schema", {})
            
            if "Tags" not in schema:
                print(f"Tags field not found in schema for component {comp_id}!")
                continue
                
            # 3. Update the Tags field options
            print(f"Updating Tags field options for component {comp_id}...")
            schema["Tags"]["options"] = new_options
            schema["Tags"]["source"] = "self" # Ensure source is explicitly self
            
            # 4. Save component
            payload = {"component": {"schema": schema}}
            resp = await client.put(comp_url, headers=headers, json=payload)
            
            if resp.status_code == 200:
                print(f"Successfully updated component {comp_id} schema with tag options.")
            else:
                print(f"Error updating component {comp_id}: {resp.status_code} {resp.text}")
                
            # Small delay
            await asyncio.sleep(0.5)

if __name__ == "__main__":
    asyncio.run(update_tags_schema())
