import numpy as np
from PIL import Image, ImageFilter
import sys
import json
import boto3
import io

show_result = False
aws_access_key_id=""
aws_secret_access_key=""
aws_session_token=""
session = None

## Can do - resize, crop, paste, other ImageFilter options

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

def convert_bw(array):
    shape = array.shape
    array = array.reshape((-1, 4))
    size = array.shape[0]
    greys = np.mean(array[:, :3], axis = 1)
    greys = greys.reshape((size, 1))
    greys = np.tile(greys, (1,3))
    array[:, :3] = greys
    array = array.reshape(shape)
    return array



def black_and_white_PIL(array):
    array = array.convert("L")
    array = array.convert("RGBA")
    return array

def blend(parameters):
    array1, array2, alpha = parameters
    array = Image.blend(array1, array2, alpha)
    return array

def blur(array):
    array = array.filter(ImageFilter.BLUR)
    return array

def dot_map(array):
    array = array.convert("1")
    return array

def compress_colors(array):
    array = array.convert("P")
    return array

def detect_edges(array):
    array = array.convert("L")
    array = array.filter(ImageFilter.FIND_EDGES)
    array = array.convert("RGBA")
    return array

def rotate_transpose(parameters):
    array, rotate, transpose = parameters
    if(transpose):
        # TODO - Get transpose working
        pass
    array = array.rotate(rotate)
    return array

def thumbnail(array):
    array.thumbnail((64,64))
    return array

def test(array):
    return array



def handle_non_standard(command, out, in_0):

    non_standard = {
        "blend": [blend, False],
        "rotate_transpose": [rotate_transpose, False],
    }

    if(command not in non_standard):
        print("Command not found")
        return

    argc = len(sys.argv)
    as_np_array = non_standard[command][1]

    if(command == "blend"):
        in_1 = str(sys.argv[4])
        array0 = read(in_0, as_np_array)
        array1 = read(in_1, as_np_array)
        alpha = 0.5
        if(argc == 6):
            alpha = float(sys.argv[5])
        parameters = [array0, array1, alpha]
    if(command == "rotate_transpose"):
        array = read(in_0, as_np_array)
        rotate = int(sys.argv[4])
        parameters = [array, rotate, True]

    array = non_standard[command][0](parameters)
    write(out, array, as_np_array)



def main(command, in_file, out_file):

    command_map = {
        "convert_bw": [convert_bw, True],
        "black_and_white_PIL": [black_and_white_PIL, False],
        "blur": [blur, False],
        "dot_map": [dot_map, False],
        "compress_colors": [compress_colors, False],
        "detect_edges": [detect_edges, False],
        "thumbnail": [thumbnail, False],
        "test": [test, False]
    }

    if(command not in command_map):
        handle_non_standard(command, out_file, in_file)
        return

    as_np_array = command_map[command][1]
    array = read(in_file, as_np_array)
    array = command_map[command][0](array)
    write(out_file, array, as_np_array)

def lambda_handler(event, context):

    command = event["command"]
    in_file = event["in_file"]
    out_file = event["out_file"]

    global aws_access_key_id, aws_secret_access_key, aws_session_token, session
    aws_access_key_id=event["aws_access_key_id"]
    aws_secret_access_key=event["aws_secret_access_key"]
    aws_session_token=event["aws_session_token"]
    session = boto3.session.Session(aws_access_key_id, aws_secret_access_key, aws_session_token)

    main(command, in_file, out_file)
    return dict(event)