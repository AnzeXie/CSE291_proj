import json
import PIL
import numpy
import socket

print('Loading function')


def lambda_handler(event, context):

    print("Received event: " + json.dumps(event, indent=2))

    # print("value1 = " + event['key1'])
    # print("value2 = " + event['key2'])
    # print("value3 = " + event['key3'])
    print("Version = " + str(event))
    response = dict()
    response["body"] = {"Value" : "Hello, World!\n" + str(event) + "\n\n" + str(event["body"]) + "\n\n" + str(event['requestContext']['http'])}
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((str(event['requestContext']['http']["sourceIp"], str(event["body"]["sender_port"])))
    # data = sock.recv(1024)
    sock.send("Hey!")
    # print(data)
    sock.close()
    return response
    # return event['key1']  # Echo back the first key value
    #raise Exception('Something went wrong')
