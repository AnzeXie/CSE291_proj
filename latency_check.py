import boto3, json, time, random

aws_access_key_id="ASIAQZ5CEJ4HBCFU6G5E"
aws_secret_access_key="wj+x4bgMXK02KVWq4QmsgcYxhJvuJZcekMuqqEap"
aws_session_token="FwoGZXIvYXdzEJf//////////wEaDDV09hJ/iXd/gmD5SSKzARmRPXGIQ0GSFEgVLeCwfYcxaAMAB02EWlx95l9AswZLL/Fr/ypGjkaw0R6MQHXj6PS7A1dKE3VOboHhJ8Tluufm4WjWV5kJM1dvwjiuLiSxQjvdg54iOe1lzCcjLt+C/K1Y+RIAtpPtl+uc3y0nopL+HwBGIClMu9ewk2C4NDgd4XwK1Xx1fs0lb4qY/GJRHmvv9rAd/ErUqEplzU5SDQjyd7F1ziZfGbpoLrTDS62QZRt9KPOQppwGMi2mVvq5CE2FFtpwBUyhi7hKSjFEGBEO7kSNpNsEgOZ3FgOb2uO821yuPY8BZKQ="

session = boto3.session.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

client = boto3.client('lambda', region_name="us-west-2",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

invoke_latencies = []
return_times = []

for i in range(2):

    time.sleep(20)
    print("Iter", i)

    start_time = time.time()

    response = client.invoke(
        FunctionName="Timer",
        InvocationType="RequestResponse"
    )

    end_time = time.time()

    payload = json.loads(response['Payload'].read())
    mid_time = payload["time"]

    invoke_latencies.append(end_time - start_time)
    return_times.append(end_time - start_time)

print(invoke_latencies, return_times)