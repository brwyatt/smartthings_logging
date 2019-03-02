import json
import logging
import os
from random import randint
from time import time

import boto3


log = logging.getLogger(__name__)

secretName = os.environ.get('SmartThingsConfigSecretName', 'SmartThingsConfig')
# secretVersion = os.environ.get('AccessTokenSecretVersion', None)
# secretStage = os.environ.get('AccessTokenSecretStage', None)
regionName = os.environ.get('Region', 'us-west-2')
cacheTimeout = int(os.environ.get('ConfigCacheTimeout', '600'))
cacheTimeoutJitter = int(os.environ.get('ConfigCacheTimeout',
                                        int(cacheTimeout/10)))

cached_config = {
    'value': {},
    'time': 0,
}


def getSmartThingsConfig(force=False):
    log.info('Fetching SmartThings config from Secrets Manager')

    if cached_config['time'] > (time() - cacheTimeout) and not force:
        log.debug('Cached config still valid, using cache!')
        return cached_config['value']

    secretsManager = boto3.client('secretsmanager', region_name=regionName)

    log.debug('Secret Name: {}'.format(secretName))
    try:
        secret = json.loads(secretsManager.get_secret_value(
            SecretId=secretName,
            # VersionId=secretVersion,
            # VersionStage=secretStage,
        )['SecretString'])
    except:
        err_msg = 'Failed to get SmartThings Config secret from Secrets Manager'
        log.critical(err_msg)
        raise Exception(err_msg)
    else:
        log.debug('Fetch complete!')
        cached_config['value'] = secret
        cached_config['time'] = time() + randint(
            0-cacheTimeoutJitter, cacheTimeoutJitter)  # Apply some randomness
        return secret
