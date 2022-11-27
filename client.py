import boto3, json, time

aws_access_key_id="ASIAQZ5CEJ4HKAAXUK6L"
aws_secret_access_key="dizpbcCkCfi/BFl3sJBH6bapaKsR9AaISuNWkT2u"
aws_session_token="FwoGZXIvYXdzEBwaDOmn/bfaIy/O2RChpiKzAYaz2zoF7mP1Ujpewj48Q30NmCqDjbaz9/7ijlg2oj9ng9flpICIOQNW610KkZ2EBFHDO9HCLVysc1+uenzu0O8Bot9rZJfkklcQnliBPY4GouewrzsM9bEuurfzdV7QRxXPDG9QTn4MNAcqpJNcaUekg90R5R+yQrtlWEOFQVeBTcX3svQGF+GN9CDX++rjTTdHJ6p0B/WEP4+/nT2xha9SskaxTFCKkDqH2OYynwlDatgAKNGQi5wGMi1UAPdORYGZwkyTyaXm+n+Nd6XqAdZSzj/MkSYNUNm6F9lFp2M1H6IwWiflfAo="

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
"command": "dot_map",
"in_file": in_file,
"out_file": out_file,
"aws_access_key_id": aws_access_key_id,
"aws_secret_access_key": aws_secret_access_key,
"aws_session_token": aws_session_token
}
client = boto3.client('lambda', region_name="us-west-2",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)
response = client.invoke(
    FunctionName="Monolith",
    InvocationType="Event",
    Payload=json.dumps(payload)
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