import uuid

import boto3
import os
from dotenv import load_dotenv

ENVIRONMENT = os.getenv("ENVIRONMENT", "prod")

if ENVIRONMENT == "prod":
  load_dotenv(".env.production")
elif ENVIRONMENT == "local":
  load_dotenv(".env.local")
else:
  load_dotenv(".env")

# AWS SQS Configuration
AWS_REGION = os.getenv("AWS_REGION")
AWS_SQS_QUEUE_URL = os.getenv("AWS_SQS_QUEUE_URL")

# Create SQS client
sqs_client = boto3.client(
  "sqs",
  region_name=AWS_REGION,
  aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


async def send_message(message_body: str, message_group_id: str):
  """
  Sends a message to AWS SQS.
  """
  try:
    response = sqs_client.send_message(
      QueueUrl=AWS_SQS_QUEUE_URL,
      MessageBody=message_body,
      MessageGroupId=message_group_id,
      MessageDeduplicationId=str(uuid.uuid4())
    )

    print("🚀 Message sent successfully 🚀")
    print({"MessageId": response["MessageId"], "Response": response})
    return True
  except Exception as e:
    print({"error": str(e)})
    return False
