import json
import boto3

show_result = False
aws_access_key_id=""
aws_secret_access_key=""
aws_session_token=""
session = None

def lambda_handler(event, context):

    commands = event["commands"]
    commands.pop(0)
    event["commands"] = commands
    if(commands == []):
        event["finished"] = True
        return event
    event["in_file"] = event["out_file"]

    event = dict(event)
    event['statusCode'] = 200
    return event
