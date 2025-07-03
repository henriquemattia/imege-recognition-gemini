import base64
import json
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from prompts import get_detailed_prompt
from google import genai
from google.genai import types
from secrets_manager import get_gemini_api_key
import mimetypes

def lambda_handler(event, context):
    api_key = get_gemini_api_key()
    client = genai.Client(api_key=api_key)
    
    try:
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        bucket = body.get('bucket')
        pic = body.get('pic')
        
        if not bucket:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing bucket'})
            }
        
        if not pic:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing pic'})
            }
        
        try:
            bucket_name = bucket.strip()
            object_key = pic.strip()
            
            if not bucket_name or not object_key:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Bucket and pic cannot be empty'})
                }
            
            s3_client = boto3.client('s3')
            
            try:
                response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
                file_content = response['Body'].read()
                
                content_type = response.get('ContentType')
                if not content_type:
                    content_type, _ = mimetypes.guess_type(object_key)
                    if not content_type:
                        content_type = 'image/jpeg'
                
                if not content_type.startswith('image/'):
                    return {
                        'statusCode': 400,
                        'body': json.dumps({'error': 'File is not an image'})
                    }
                
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == 'NoSuchBucket':
                    return {
                        'statusCode': 404,
                        'body': json.dumps({'error': 'S3 bucket not found'})
                    }
                elif error_code == 'NoSuchKey':
                    return {
                        'statusCode': 404,
                        'body': json.dumps({'error': 'S3 object not found'})
                    }
                elif error_code == 'AccessDenied':
                    return {
                        'statusCode': 403,
                        'body': json.dumps({'error': 'Access denied to S3 object'})
                    }
                else:
                    return {
                        'statusCode': 500,
                        'body': json.dumps({'error': f'S3 error: {str(e)}'})
                    }
            except NoCredentialsError:
                return {
                    'statusCode': 500,
                    'body': json.dumps({'error': 'AWS credentials not configured'})
                }
            
        except Exception as e:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': f'Error processing S3 request: {str(e)}'})
            }
            
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