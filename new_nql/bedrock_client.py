import boto3
import json

DEFAULT_BR_MODEL = "anthropic.claude-3-5-sonnet-20240620-v1:0"
# DEFAULT_BR_MODEL = "anthropic.claude-3-5-haiku-20241022-v1:0"


class BedrockApiClient():
    """
    Cliente para AWS Bedrock
    """

    def __init__(self, model=DEFAULT_BR_MODEL):
        self.model = model
        self.runtime = boto3.client("bedrock-runtime", region_name="us-east-1")


    def chat_completion(self, messages, temp):
        bedrock_runtime = self.runtime

        body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "temperature": temp,
        "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"{messages}"},
                    ],
                }
            ],
        }
        
        response = bedrock_runtime.invoke_model(
            modelId = DEFAULT_BR_MODEL,
            contentType =  "application/json",
            accept = "application/json",
            body = json.dumps(body)
        )


        input_tokens = response["ResponseMetadata"]["HTTPHeaders"]["x-amzn-bedrock-input-token-count"]
        output_tokens = response["ResponseMetadata"]["HTTPHeaders"]["x-amzn-bedrock-output-token-count"]
        latency = response["ResponseMetadata"]["HTTPHeaders"]["x-amzn-bedrock-invocation-latency"]
        total_tokens = int(input_tokens) + int(output_tokens)
        response_body = json.loads(response["body"].read())

        response_text = response_body["content"][0]["text"]

        with open("token_trace.csv", 'a', encoding='utf-8') as f:
            messages_ = str(messages).replace("\n", "\\n")
            response_text_ = response_text.replace("\n", "\\n")
            f.write(f'{messages_}¡{response_text_}¡{input_tokens}¡{output_tokens}¡{total_tokens}¡{latency}')
            f.write("\n")


        return response_text
