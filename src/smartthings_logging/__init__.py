import logging

from smartthings_logging.cloudwatch import sendLogs
from smartthings_logging.smartthings import getData


log = logging.getLogger(__name__)


def collect_and_log(device_types=None):
    log_data(collect(device_types))


def collect(device_types=None):
    log.info('Collecting data from SmartThings')
    if device_types is None:
        # Default device types
        device_types = ['temperature', 'humidity', 'battery', 'power', 'energy',
                        'voltage']
    log.debug('Device Types to collect: {}'.format(device_types))

    aggregate_data = {}

    for device_type in device_types:
        log.debug('Collecting device type {}'.format(device_type))
        data = getData(device_type)
        for device_name in data:
            log.debug('Parsing data for {}::{}'.format(device_type,
                                                       device_name))
            if device_name not in aggregate_data:
                aggregate_data[device_name] = {}
            aggregate_data[device_name][device_type] = {
                'value': data[device_name]['state']
            }

    log.info('Collection complete')
    return aggregate_data


def log_data(aggregate_data):
    sendLogs(aggregate_data)
