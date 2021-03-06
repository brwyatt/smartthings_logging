from datetime import datetime
import logging
import os
from time import time

import boto3


log = logging.getLogger(__name__)

logGroupName = os.environ.get('LogGroup', 'SmartThings')
regionName = os.environ.get('Region', 'us-west-2')
metricNamespace = os.environ.get('MetricNamespace', 'SmartThings')


def sendLogs(data):
    log.info('Logging SmartThings data to CloudWatch Logs')
    cwlogs = boto3.client('logs', region_name=regionName)

    t = int(time() * 1000)

    for logStreamName in data:
        # Create the logEvents list to send
        logEvents = [{
            'timestamp': t,
            'message': '{{ "name": "{0}", "type": "{1}", "value": {2} }}'
            .format(logStreamName, x, data[logStreamName][x]['value'])
        } for x in data[logStreamName]]

        # Check if LogStream exists, create if needed
        logStreams = cwlogs.describe_log_streams(
            logGroupName=logGroupName,
            logStreamNamePrefix=logStreamName
        )['logStreams']

        if logStreamName not in [x['logStreamName'] for x in logStreams]:
            log.debug('LogStream "{}" does not exist, creating!'
                      .format(logStreamName))
            cwlogs.create_log_stream(
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

        log.debug('Putting LogEvent for {}'.format(logStreamName))
        cwlogs.put_log_events(**request)

    # Create MetricFilters if needed
    filters = [x['filterName'] for x in cwlogs.describe_metric_filters(
        logGroupName=logGroupName
    )['metricFilters']]
    for device_name in data:
        for device_type in data[device_name]:
            filterName = '{0} - {1}'.format(device_name, device_type)
            if filterName not in filters:
                log.debug('Metric filter "{}" does not exist, creating!'
                          .format(filterName))
                cwlogs.put_metric_filter(
                    logGroupName=logGroupName,
                    filterName=filterName,
                    filterPattern='{{$.name = "{0}" && $.type = "{1}" && '
                    '$.value = *}}'.format(device_name, device_type),
                    metricTransformations=[
                        {
                            'metricName': filterName,
                            'metricNamespace': metricNamespace,
                            'metricValue': '$.value'
                        }
                    ]
                )

    log.debug('Done logging LogEvents')


def sendMetrics(data):
    log.info('Logging SmartThings data to CloudWatch Metrics')
    cw = boto3.client('cloudwatch', region_name=regionName)

    timestamp = datetime.utcnow()

    for sensorName in data:
        log.debug('Putting Metrics for {}'.format(sensorName))
        cw.put_metric_data(
            Namespace=metricNamespace,
            MetricData=[
                {
                    'MetricName': metricName,
                    'Dimensions': [
                        {
                            'Name': 'SensorName',
                            'Value': sensorName,
                        },
                    ],
                    'Timestamp': timestamp,
                    'Unit': 'None',
                    'Value': metricData['value'],
                } for metricName, metricData in data[sensorName].items()
            ]
        )

    log.debug('Done logging Metrics')
