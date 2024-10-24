# Task

Develop a serverless API using AWS services that manages a simple inventory system. The API will handle creating, retrieving, updating, and deleting inventory items stored in a DynamoDB table. Each item will have an id, name, description, and quantity.

# Steps to Complete the Task:

 ## 1. Set Up AWS Environment
 - Create an AWS account if you don’t already have one.
 - Set up IAM roles that give your Lambda functions permission to access DynamoDB and other necessary services.
 
 ## 2. Define the Data Model
 - Design the DynamoDB table for your inventory items.
 - Define the primary key as id and other attributes like name, description, and quantity.

 ## 3. Develop Lambda Functions
 - Write separate Lambda functions for each CRUD operation:
 - POST /items to add new items.
 - GET /items and GET /items/{id} to retrieve items.
 - PUT /items/{id} to update an item.
 - DELETE /items/{id} to delete an item.
 - Test these functions locally using AWS SAM or the AWS CLI.

 ## 4. Set Up API Gateway
 - Create a new API in AWS API Gateway.
 - Set up resources and methods for /items and /items/{id}.
 - Link these methods to the respective Lambda functions.
 - Enable CORS if your API will be accessed from a web application.

 ## 5. Integrate API with Lambda
 - Ensure each method in API Gateway correctly passes data to the Lambda functions.

 ## 6. Deploy API
 - Deploy your API in API Gateway.
 - Test the API using Postman or cURL to ensure all endpoints work as expected.

 ## 7. Optional - Create a Frontend
 - Develop a frontend application using frameworks like React or Angular.
 - Host the frontend on AWS S3 and distribute it via AWS CloudFront.
 - Ensure the frontend can interact with the API.

 ## 8. Monitor and Optimize
 - Monitor the performance and logs of your API and Lambda functions using AWS CloudWatch.
 - Optimize the Lambda functions and API based on performance data.
