import json
import boto3

show_result = False
aws_access_key_id=""
aws_secret_access_key=""
aws_session_token=""
session = None

def handle_non_standard(command, out, in_0):

    non_standard = {
        "blend": "Default",
        "rotate_transpose": "Default",
    }

    if(command not in non_standard):
        print("Command not found -", command)
        return "failure", None
    return "success", non_standard[command]

def main(command, in_file, out_file):

    command_map = {
        "black_and_white_PIL": "BlackWhite",
        "blur": "Blur",
        "dot_map": "DotMap",
        "compress_colors": "CompressColors",
        "detect_edges": "DetectEdges",
        "thumbnail": "Thumbnail",
        "test": "Test"
    }

    if(command not in command_map):
        status, lambd = handle_non_standard(command, out_file, in_file)
        return status, lambd
    return "success", command_map[command]

def lambda_handler(event, context):

    command = event["command"]
    in_file = event["in_file"]
    out_file = event["out_file"]

    global aws_access_key_id, aws_secret_access_key, aws_session_token, session
    aws_access_key_id=event["aws_access_key_id"]
    aws_secret_access_key=event["aws_secret_access_key"]
    aws_session_token=event["aws_session_token"]
    session = boto3.session.Session(aws_access_key_id, aws_secret_access_key, aws_session_token)

    event["status"], event["next"] = main(command, in_file, out_file)
    event = dict(event)
    event['statusCode'] = 200
    return event
