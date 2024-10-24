import json
import boto3
import uuid

'''
Expected event json
{
  "http_method":"POST",
  "body": {
    "name": "name2",
    "description": "description2",
    "quantity": 22
  },
  "path_parameters": {
        "id": "1017b930-c345-4814-9c70-fbb5c03e2ece"
    }
  
}
{
  "http_method":"DELETE",
  "path_parameters": {
        "id": "1017b930-c345-4814-9c70-fbb5c03e2ece"
    }
  
}
'''

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')


def lambda_handler(event, context):
    http_method = event.get('http_method', '')
    item_id = event['path_parameters'].get('id') if 'path_parameters' in event and event['path_parameters'] is not None else ''
    
    if http_method == 'POST':
        return create_item(event)
    elif http_method == 'GET':
        if item_id:
            return get_item(item_id)
        else:
            return get_all_items()
    elif http_method == 'PUT':
        return update_item(item_id, event)
    elif http_method == 'DELETE':
        return delete_item(item_id)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Unsupported HTTP method')
        }

def create_item(event):
    item_id = str(uuid.uuid4())
    body = event['body']
    item = {
        'id': item_id,
        'name': body['name'],
        'description': body['description'],
        'quantity': body['quantity']
    }
    table.put_item(Item=item)
    return {
        'statusCode': 200,
        'body': json.dumps('Item created successfully!')
    }

def get_all_items():
    response = table.scan()
    items = response.get('Items', [])
    return {
        'statusCode': 200,
        'body': items
    }

def get_item(item_id):
    response = table.get_item(Key={'id': item_id})
    item = response.get('Item', {})
    return {
        'statusCode': 200,
        'body': item
    }

def update_item(item_id, event):
    body = event['body']
    update_expression = 'SET #nameAttr = :name, #descriptionAttr = :description, #quantityAttr = :quantity'
    
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
        table.update_item(
            Key={'id': item_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Item updated successfully!')
        }
    
    except Exception as e:
        # Handle the exception and return a meaningful error message
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error updating item: {str(e)}')
        }

def delete_item(item_id):
    table.delete_item(Key={'id': item_id})
    return {
        'statusCode': 200,
        'body': json.dumps('Item deleted successfully!')
    }
