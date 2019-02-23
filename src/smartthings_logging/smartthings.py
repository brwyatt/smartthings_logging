import json

from smartthings_cli import smartthings_cli

from .s3 import getConfig


def getData(device_type):
    config = json.loads(getConfig('smartthings-logging-config',
                                  'smartthings_cli.json'))

    access_token = config['access_token']
    endpoint_base_url, endpoint_url = smartthings_cli.get_endpoint_url(
        access_token)

    return smartthings_cli.get_status(access_token, endpoint_base_url,
                                      endpoint_url, device_type)
