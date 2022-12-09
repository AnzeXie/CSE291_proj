import boto3, json, time

aws_access_key_id="ASIAQZ5CEJ4HEPTVXI54"
aws_secret_access_key="xhrz3MZKhaFffOa55hVbLJlRL0y5rIDHDPqg53fd"
aws_session_token="FwoGZXIvYXdzEF8aDA/velw3yyFBNWpMHCKzAW73mqgs8/vQ/rSRSNPGilGRdZG9sPZH+nc3MzMkcu4HHp74jGeQAkSxbgc4Tb1CgQz2Lxjdlg7f3ub2CU/4mVGGk5ClI3fvw+t1T5Az1bXxhc2YzM+jKzlIXS5WHuBKoEYrGCnCNS9UUa+AdT5e1CuFzW82ci4vvf8j3QYyVn8p96G+B5HImFcjiPcL9otxgugpMIzUIhY3S3x57DDk3KjidI5IEaEMWvZYtteCJnzuG0UlKJT0mZwGMi11hRQbqMD68zdwmNDJAnrnBEjVy2Pw5n0ZgNRU/cN7R/bN9R+YC4v0+POW+Ms="

session = boto3.session.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

print("Enter command (default dot_map):")
command = str(input())
if(not command):
    command = "dot_map"
print("Enter in file (default backup.png):")
in_file = str(input())
if(not in_file):
    in_file = "backup.png"
print("Enter out file (default auto generate):")
out_file = str(input())
if(not out_file):
    out_file = "out_" + str(time.time()) + "_" + in_file

print("Reading in file")
f = open(in_file, "rb")
data = f.read()
f.close()

print("Uploading input")
s3 = session.resource('s3')
object = s3.Object('imageagent', in_file)
object.put(Body=data)

print("Requesting lambda")
payload = {
"command": command,
"in_file": in_file,
"out_file": out_file,
"aws_access_key_id": aws_access_key_id,
"aws_secret_access_key": aws_secret_access_key,
"aws_session_token": aws_session_token
}
client = boto3.client('stepfunctions', region_name="us-west-2",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)
# response = client.start_execution(
#     stateMachineArn="arn:aws:states:us-west-2:055637724942:stateMachine:Attempt0",
#     input=json.dumps(payload)
# )
response = client.start_execution(
    stateMachineArn="arn:aws:states:us-west-2:055637724942:stateMachine:Attempt1",
    input=json.dumps(payload)
)

print("Received acknowledgement")

data = ""
for i in range(15):
    time.sleep(1)
    try:
        obj = s3.Object('imageagent', out_file)
        data = obj.get()["Body"].read()
        print("Success getting " + out_file)
        break
    except:
        print("Sleeping 1")
        continue

if(not data):
    print("Aborting")
else:
    print("Saving output")
    f = open(out_file, "wb")
    f.write(data)
    f.close()

print("Done")