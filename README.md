# LinkShrink — Serverless URL Shortener

### https://github.com/swanandihelambe/LinkShrink

LinkShrink is a serverless URL shortener built using AWS services. It converts a long URL into a short code and redirects users to the original URL when the short code is accessed.

## Project Overview

The project demonstrates how to build a lightweight API using AWS Lambda, Amazon API Gateway, and Amazon DynamoDB without managing a traditional server.

## Architecture

Client → Amazon API Gateway → AWS Lambda → Amazon DynamoDB

- **Amazon API Gateway:** Receives HTTP requests and routes them to Lambda.
- **AWS Lambda:** Validates URLs, generates short codes, stores URL mappings, and handles redirects.
- **Amazon DynamoDB:** Stores short codes and their corresponding original URLs.
- **AWS IAM:** Controls the permissions required by Lambda to access DynamoDB.
- **Amazon CloudWatch:** Stores Lambda execution logs for monitoring and troubleshooting.

## Features

- Generates six-character alphanumeric short codes.
- Validates URLs using HTTP and HTTPS schemes.
- Stores URL mappings in DynamoDB.
- Checks for existing short codes before saving a new mapping.
- Redirects users to the original URL.
- Handles invalid requests and unknown short codes.
- Uses serverless AWS services.

## API Endpoints

| Method | Endpoint | Description | Expected result |
|---|---|---|---|
| POST | `/shorten` | Creates a short code for a URL | `201 Created` |
| GET | `/{short_code}` | Redirects to the original URL | `302 Found` |

### Example request

`POST /shorten`

```json
{
  "url": "https://example.com"
}
```

### Example response

```json
{
  "short_code": "aB12xY"
}
```

The short code shown above is an example; actual codes are generated dynamically.

## Error Handling

| Status code | Meaning |
|---|---|
| `400` | Missing or invalid request data |
| `404` | Short code not found |
| `405` | Unsupported HTTP method |

## Testing

The project was tested for:

- Successful URL shortening
- Missing URL input
- Invalid URL input
- Redirecting using an existing short code
- Handling a nonexistent short code

Lambda execution logs were also checked using Amazon CloudWatch.

## Technologies Used

- Python
- AWS Lambda
- Amazon API Gateway
- Amazon DynamoDB
- AWS IAM
- Amazon CloudWatch

## Project Status

The implementation and functional testing were completed in AWS. The AWS resources have since been deleted to avoid ongoing charges. This repository documents the source code and project implementation; the API is not currently deployed.

## Learning Outcomes

- Building HTTP APIs with API Gateway and Lambda
- Working with DynamoDB using `boto3`
- Implementing URL validation and HTTP redirects
- Applying IAM permissions to AWS services
- Testing serverless functions and reviewing CloudWatch logs
