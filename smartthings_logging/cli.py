import sys

from smartthings_cli import smartthings_cli

from smartthings_logging.cloudwatch import sendLogs


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    config = smartthings_cli.load_config()

    access_token = config['access_token']
    endpoint_base_url, endpoint_url = smartthings_cli.get_endpoint_url(
        access_token)

    device_type = 'temperature'

    results = smartthings_cli.get_status(access_token, endpoint_base_url,
                                         endpoint_url, device_type)

    sendLogs(device_type, results)


if __name__ == '__main__':
    main()
