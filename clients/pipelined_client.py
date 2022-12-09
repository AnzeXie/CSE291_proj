import boto3, json, time

aws_access_key_id="ASIAQZ5CEJ4HMR6G5UUM"
aws_secret_access_key="vmRMRsrcMp0oXWmATF6LHeF8PBI0okYjAZ+iUq7O"
aws_session_token="FwoGZXIvYXdzED0aDLOum9tNtc83hgwWliKzAUxoNSY6vBcumSIUaaPdtk9BUMEK0yzmyFkmCj7ryd7RTzwNrLwT0yr4Do9u+quhKKzKiNYcycSAP8kPQP+r3gIMHPG3+HkTPdGMFcdG2PFZZXaOavlgarcJFOG+qjR8S8sQhLGlzm6hL/JxDR305S3k2uB/7Fehaz8cLWcRl9ODk977sImjYPeW2L6fn/JOXlN0ch41a+e78yxPX2ftK5zoEjSrHt9X2i6bwgHF5dIkBE68KLLLypwGMi1KOlWOSwr6EnvtArnOwSnw4rHZJnaXN30mDUOAGNJN75NW6mDZ5JtMNQlpsWM="

session = boto3.session.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

commands = ["compress_colors", "thumbnail"]
print("Enter command (default dot_map):")
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
"commands": commands,
"in_file": in_file,
"final_out_file": out_file,
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
    stateMachineArn="arn:aws:states:us-west-2:055637724942:stateMachine:Attempt_Pipelined",
    input=json.dumps(payload)
)

print("Received acknowledgement")

data = ""
for i in range(30):
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