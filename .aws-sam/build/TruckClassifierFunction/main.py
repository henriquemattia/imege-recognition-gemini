import base64
import json
import boto3
from botocore.exceptions import ClientError
from prompts import get_detailed_prompt
from google import genai
from google.genai import types
from secrets_manager import get_gemini_api_key

def lambda_handler(event, context):
    api_key = get_gemini_api_key()
    client = genai.Client(api_key=api_key)
    
    try:
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        image_base64 = body.get('image_base64')
        if not image_base64:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing image_base64'})
            }
        
        if image_base64.startswith('data:'):
            image_base64 = image_base64.split(',')[1]
        
        image_base64 = image_base64.strip()
        
        padding = 4 - len(image_base64) % 4
        if padding != 4:
            image_base64 += '=' * padding
        
        try:
            file_content = base64.b64decode(image_base64)
        except Exception as e:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': f'Invalid base64: {str(e)}'})
            }
        
        content_type = body.get('content_type', 'image/jpeg')
        base64_encoded = base64.b64encode(file_content).decode('utf-8')
        
        image = types.Part.from_bytes(
            data=base64_encoded,
            mime_type=content_type,
        )
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[image, get_detailed_prompt()]
        )
        
        import re
        cleaned = re.sub(r'```json\s*|\s*```', '', response.text).strip()
        result = json.loads(cleaned)
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }