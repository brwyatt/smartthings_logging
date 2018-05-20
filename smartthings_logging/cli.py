import sys

from smartthings_logging.cloudwatch import sendLogs
from smartthings_logging.smartthings import getData


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    aggregate_data = {}

    for device_type in ['temperature', 'humidity', 'battery']:
        data = getData(device_type)
        for device_name in data:
            if device_name not in aggregate_data:
                aggregate_data[device_name] = {}
            aggregate_data[device_name][device_type] = {
                'value': data[device_name]['state']
            }

    sendLogs(aggregate_data)


if __name__ == '__main__':
    main()
