import sys

from smartthings_logging.cloudwatch import sendLogs
from smartthings_logging.smartthings import getData


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    for device_type in ['temperature', 'humidity', 'battery']:
        sendLogs(device_type, getData(device_type))


if __name__ == '__main__':
    main()
