import json
import boto3
from botocore.exceptions import ClientError

from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Inventory')
    query_params = event.get('queryStringParameters')
    # Check if query parameters are present
    if query_params is None:
        response = table.scan()
        items = response.get('Items', [])
        return {
            'statusCode': 200,
            'body': json.dumps(items, cls=DecimalEncoder)
        }
    item_id = query_params.get('id')
    try:
        response = table.get_item(Key={'id': item_id})
        item = response.get('Item', {})

        if 'Item' in response:
            return {
                'statusCode': 200,
                'body': json.dumps(item, cls=DecimalEncoder)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps('Item not found')
            }
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing parameter: id')
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
