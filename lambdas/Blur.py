from PIL import Image, ImageFilter
import json
import boto3
import io

show_result = False
aws_access_key_id=""
aws_secret_access_key=""
aws_session_token=""
session = None

def read(path, as_np_array = True):

    print("Reading " + path + " from S3 with " + aws_access_key_id + " and " + aws_secret_access_key)
    s3 = session.resource("s3")
    obj = s3.Object('imageagent', path)
    data = obj.get()["Body"].read()
    data = Image.open(io.BytesIO(data))
    if(as_np_array):
        data.load()
        array = np.asarray(data)
    else:
        array = data
    return array

def write(path, array, as_np_array = True):
    if(as_np_array):
        data = Image.fromarray(array, "RGBA")
    else:
        data = array
    output = io.BytesIO()
    data.save(output, "PNG")
    data = output.getvalue()
    s3 = session.resource("s3")
    obj = s3.Object('imageagent', path)
    obj.put(Body=data)

def blur(array):
    array = array.filter(ImageFilter.BLUR)
    return array

def lambda_handler(event, context):

    in_file = event["in_file"]
    out_file = event["out_file"]

    global aws_access_key_id, aws_secret_access_key, aws_session_token, session
    aws_access_key_id=event["aws_access_key_id"]
    aws_secret_access_key=event["aws_secret_access_key"]
    aws_session_token=event["aws_session_token"]
    session = boto3.session.Session(aws_access_key_id, aws_secret_access_key, aws_session_token)
    array = read(in_file, False)
    array = blur(array)
    write(out_file, array, False)

    return dict(event)