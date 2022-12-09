This folder contains resources for measuring the latency of triggering a lambda -\
\
lambda_timer - A simple lambda function that returns its own startup time (We observe significant clock differences between AWS and NTP, so the results of these are not very reliable)\
latency_check.py - A simple client that waits for lambda execution to complete and collects its results, this is used to time the total execution duration\