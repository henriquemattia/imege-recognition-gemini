import os
import boto3
import json

def get_secret():
    secret_name = "px-labs-sm"
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        secret = get_secret_value_response['SecretString']
        
        try:
            secret_dict = json.loads(secret)
            return secret_dict.get('GEMINI_API_KEY')
        except:
            return secret
            
    except ClientError as e:
        raise e

def get_gemini_api_key():
    local_key = os.getenv('GEMINI_API_KEY')
    if local_key:
        print("Using local GEMINI_API_KEY")
        return local_key
    
    try:
        api_key = get_secret()
        return api_key
    except Exception as e:
        raise ValueError(f"Could not retrieve API key: {str(e)}")
