import logging

from smartthings_cli import smartthings_cli

from smartthings_logging.secretsmanager import getSmartThingsConfig


log = logging.getLogger(__name__)


def getData(device_type):
    log.info('Getting data for device type "{}"'.format(device_type))
    config = getSmartThingsConfig()

    access_token = config['access_token']
    endpoint_base_url, endpoint_url = smartthings_cli.get_endpoint_url(
        access_token)

    status = smartthings_cli.get_status(access_token, endpoint_base_url,
                                        endpoint_url, device_type)
    log.debug('Result from SmartThings API: {}'.format(status))
    return status
