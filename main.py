import base64
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from prompts import get_detailed_prompt, get_optimized_prompt
from google import genai
from google.genai import types
import json
import re

app = FastAPI()
client = genai.Client()


@app.post("/upload-file")
async def upload_with_validation(file: UploadFile = File(...)):
    # Validate file type
    try:
        allowed_types = ["image/jpeg", "image/png", "application/pdf"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="File type not allowed")
        
        # Validate file size (e.g., max 5MB)
        file_content = await file.read()
        if len(file_content) > 20 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large, max is 20mb")
        
        # Convert to base64
        base64_encoded = base64.b64encode(file_content).decode('utf-8')
        
        image = types.Part.from_bytes(
            data=base64_encoded,
            mime_type=file.content_type,
        )
        
        response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            image,
            get_detailed_prompt()
        ]
    )
        
        return clean_json_response(response.text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
    
def clean_json_response(text):
    # Remove the ```json and ``` wrapper
    cleaned = re.sub(r'```json\s*|\s*```', '', text).strip()
    return json.loads(cleaned)