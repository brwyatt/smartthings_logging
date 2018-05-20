from time import time

import boto3

logGroupName = 'SmartThings'
regionName = 'us-west-2'


def sendLogs(logStreamName, data):
    now = int(time() * 1000)

    # Create the logEvents list to send
    logEvents = [{
        'timestamp': now,
        'message': '{{ "name": "{0}", "value": {1} }}'.format(
            x, data[x]['state'])
    } for x in data]

    logs = boto3.client('logs', region_name=regionName)

    # Check if LogGroup exists, create if needed
    logGroups = logs.describe_log_groups(
        logGroupNamePrefix=logGroupName)['logGroups']

    if logGroupName not in [x['logGroupName'] for x in logGroups]:
        logs.create_log_group(logGroupName=logGroupName)

    # Check if LogStream exists, create if needed
    logStreams = logs.describe_log_streams(
        logGroupName=logGroupName,
        logStreamNamePrefix=logStreamName
    )['logStreams']

    if logStreamName not in [x['logStreamName'] for x in logStreams]:
        logs.create_log_stream(
            logGroupName=logGroupName,
            logStreamName=logStreamName
        )
        sequenceToken = None
    else:
        # Set LogStream's SequenceToken
        sequenceToken = [x for x in logStreams
                         if x['logStreamName'] == logStreamName][0].get(
                             'uploadSequenceToken', None)

    # Send the logs to CloudWatch
    request = {
        'logGroupName': logGroupName,
        'logStreamName': logStreamName,
        'logEvents': logEvents
    }

    if sequenceToken:
        request['sequenceToken'] = sequenceToken

    logs.put_log_events(**request)
