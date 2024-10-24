import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Inventory')
    try:
        query_params = event.get('queryStringParameters')
    
        # Check if query parameters are present
        if query_params is None:
            return {
                'statusCode': 400,
                'body': json.dumps('Missing query parameters')
            }
        item_id = query_params.get('id')
        response = table.delete_item(
            Key={'id': item_id},
            ReturnValues='ALL_OLD'
        )
        if 'Attributes' in response:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Item deleted successfully!',
                })
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
