#!/usr/bin/env python3

import boto3
import json
from botocore.config import Config

# Create the Bedrock Runtime client with extended timeout
session = boto3.Session(region_name='us-east-1')
client = session.client(
    'bedrock-runtime',
    config=Config(read_timeout=3600)
)

question = 'Search Google Trends for the latest trends for January 2026. Top 10 topics.'
conversation = [
   {
     "role": "user",
     "content": [{"text": question}],
   }
]

# Use Nova 2 model ()
model_id = "us.amazon.nova-2-lite-v1:0"
print("=============start-----")
print("Without Web Grounding")
print("=" * 50)
response = client.converse(
    modelId=model_id,
    messages=conversation,
)
print(json.dumps(response['output'], indent=2))

print("\n\nWith Web Grounding")
print("=" * 50)

# Define the tool configuration for web grounding
tool_config = {
    "tools": [{
        "systemTool": {
            "name": "nova_grounding"
        }
    }]
}

response = client.converse(
    modelId=model_id,
    messages=conversation,
    toolConfig=tool_config
)

# Extract text with interleaved citations
output_with_citations = ""
content_list = response["output"]["message"]["content"]
for content in content_list:
    if "text" in content:
        output_with_citations += content["text"]
    elif "citationsContent" in content:
        citations = content["citationsContent"]["citations"]
        for citation in citations:
            url = citation["location"]["web"]["url"]
            output_with_citations += f" [{url}]"

print(output_with_citations)
print("\n\nFull Response:")
print(json.dumps(response['output'], indent=2))
