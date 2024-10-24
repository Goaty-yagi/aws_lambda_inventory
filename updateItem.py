import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Inventory')
    query_params = event.get('queryStringParameters')
    # Check if query parameters are present
    if query_params is None:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing query parameters')
        }
    item_id = query_params.get('id')

    body = event.get('body')
    if body is None:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid JSON body: body is None')
        }
    update_expression = 'SET #nameAttr = :name, #descriptionAttr = :description, #quantityAttr = :quantity'
    try:
        body = json.loads(body)
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid JSON body')
        }

    required_fields = ['name', 'description', 'quantity']
    for field in required_fields:
        if field not in body:
            return {
                'statusCode': 400,
                'body': json.dumps(f'Missing parameter: {field} {body}')
            }

    # Define the attribute values
    expression_attribute_values = {
        ':name': body['name'],
        ':description': body['description'],
        ':quantity': body['quantity']
    }
    
    # Define the expression attribute names mapping the placeholders to actual attribute names
    expression_attribute_names = {
        '#nameAttr': 'name',
        '#descriptionAttr': 'description',
        '#quantityAttr': 'quantity'
    }
    
    try:
        # Update the item
        response = table.update_item(
            Key={'id': item_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
        ReturnValues="ALL_OLD"
        )

        if 'Attributes' in response:
            message = 'Item updated successfully!'
            status_code = 200
        else:
            message = 'Item created successfully!'
            status_code = 201
        
        return {
            'statusCode': status_code,
            'body': message
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
        