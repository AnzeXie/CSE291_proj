import boto3, json, time

aws_access_key_id="ASIAQZ5CEJ4HBCFU6G5E"
aws_secret_access_key="wj+x4bgMXK02KVWq4QmsgcYxhJvuJZcekMuqqEap"
aws_session_token="FwoGZXIvYXdzEJf//////////wEaDDV09hJ/iXd/gmD5SSKzARmRPXGIQ0GSFEgVLeCwfYcxaAMAB02EWlx95l9AswZLL/Fr/ypGjkaw0R6MQHXj6PS7A1dKE3VOboHhJ8Tluufm4WjWV5kJM1dvwjiuLiSxQjvdg54iOe1lzCcjLt+C/K1Y+RIAtpPtl+uc3y0nopL+HwBGIClMu9ewk2C4NDgd4XwK1Xx1fs0lb4qY/GJRHmvv9rAd/ErUqEplzU5SDQjyd7F1ziZfGbpoLrTDS62QZRt9KPOQppwGMi2mVvq5CE2FFtpwBUyhi7hKSjFEGBEO7kSNpNsEgOZ3FgOb2uO821yuPY8BZKQ="

session = boto3.session.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

commands = ["blur", "black_and_white_PIL", "detect_edges"]
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