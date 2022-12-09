import json, time

def lambda_handler(event, context):
    current = time.time()
    response = dict()
    response['time'] = current
    return response