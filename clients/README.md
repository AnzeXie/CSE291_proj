This folder contains the three clients implemented at various stages of the project -

client.py - a basic client capable of accessing S3 and directly triggering lambdas
step_client.py - a more advanced version that triggers step functions instead of lambdas, also capable of S3 access
pipelined_client.py - the final version, capable of triggering step functions and giving multiple commands in a single call rather than a single one