import json
import random
import string
from urllib.parse import urlparse

import boto3


# DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("LinkShrinkURLs")


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=length))


def is_valid_url(url):
    try:
        parsed = urlparse(url)

        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
        )

    except Exception:
        return False


def response(status_code, body=None, headers=None):
    return {
        "statusCode": status_code,
        "headers": headers or {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body) if body is not None else ""
    }


def lambda_handler(event, context):

    method = event.get("requestContext", {}).get("http", {}).get("method", "")
    path_parameters = event.get("pathParameters") or {}

    # ==========================================
    # POST /shorten
    # ==========================================

    if method == "POST":

        try:
            body = json.loads(event.get("body") or "{}")

        except json.JSONDecodeError:
            return response(
                400,
                {"error": "Invalid JSON"}
            )

        original_url = body.get("url")

        # Missing URL
        if not original_url:
            return response(
                400,
                {"error": "URL is required"}
            )

        # URL must be a string
        if not isinstance(original_url, str):
            return response(
                400,
                {"error": "URL must be a string"}
            )

        # Validate URL
        if not is_valid_url(original_url):
            return response(
                400,
                {"error": "Invalid URL. Use http:// or https://"}
            )

        # Generate a unique short code
        while True:

            short_code = generate_short_code()

            existing = table.get_item(
                Key={"short_code": short_code}
            )

            if "Item" not in existing:
                break

        # Store URL mapping
        table.put_item(
            Item={
                "short_code": short_code,
                "original_url": original_url
            }
        )

        return response(
            201,
            {
                "short_code": short_code
            }
        )

    # ==========================================
    # GET /{short_code}
    # ==========================================

    if method == "GET":

        short_code = path_parameters.get("short_code")

        if not short_code:
            return response(
                400,
                {"error": "Short code is required"}
            )

        result = table.get_item(
            Key={"short_code": short_code}
        )

        item = result.get("Item")

        # Short code doesn't exist
        if not item:
            return response(
                404,
                {"error": "Short URL not found"}
            )

        # Redirect
        return {
            "statusCode": 302,
            "headers": {
                "Location": item["original_url"]
            },
            "body": ""
        }

    # ==========================================
    # Unsupported method
    # ==========================================

    return response(
        405,
        {"error": "Method not allowed"}
    )
