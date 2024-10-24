import json
import boto3
import uuid
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Inventory')

    try:
        body = event.get('body')
        if body is None:
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid JSON body: body is None')
            }
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid JSON body')
            }
        item = {
            'id': str(uuid.uuid4()),
            'name': body['name'],
            'description': body['description'],
            'quantity': body['quantity']
        }

        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps('Item added successfully!')
        }
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Missing parameter: {str(e)}')
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Internal server error: {e.response["Error"]["Message"]}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'An error occurred: {str(e)}')
        }
