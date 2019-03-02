import os
from time import time

import boto3

logGroupName = os.environ.get('LogGroup', 'SmartThings')
regionName = os.environ.get('Region', 'us-west-2')


def sendLogs(data):

    logs = boto3.client('logs', region_name=regionName)

    # Check if LogGroup exists, create if needed
    logGroups = logs.describe_log_groups(
        logGroupNamePrefix=logGroupName)['logGroups']

    if logGroupName not in [x['logGroupName'] for x in logGroups]:
        logs.create_log_group(logGroupName=logGroupName)

    t = int(time() * 1000)

    for logStreamName in data:
        # Create the logEvents list to send
        logEvents = [{
            'timestamp': t,
            'message': '{{ "name": "{0}", "type": "{1}", "value": {2} }}'
            .format(logStreamName, x, data[logStreamName][x]['value'])
        } for x in data[logStreamName]]

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

    # Create MetricFilters if needed
    filters = [x['filterName'] for x in logs.describe_metric_filters(
        logGroupName=logGroupName
    )['metricFilters']]
    for device_name in data:
        for device_type in data[device_name]:
            filterName = '{0} - {1}'.format(device_name, device_type)
            if filterName not in filters:
                logs.put_metric_filter(
                    logGroupName=logGroupName,
                    filterName=filterName,
                    filterPattern='{{$.name = "{0}" && $.type = "{1}" && '
                    '$.value = *}}'.format(device_name, device_type),
                    metricTransformations=[
                        {
                            'metricName': filterName,
                            'metricNamespace': logGroupName,
                            'metricValue': '$.value'
                        }
                    ]
                )
