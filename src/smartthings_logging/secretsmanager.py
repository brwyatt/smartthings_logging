import json
import logging
import os

import boto3


log = logging.getLogger(__name__)

secretName = os.environ.get('SmartThingsConfigSecretName', 'SmartThingsConfig')
# secretVersion = os.environ.get('AccessTokenSecretVersion', None)
# secretStage = os.environ.get('AccessTokenSecretStage', None)
regionName = os.environ.get('Region', 'us-west-2')


def getSmartThingsConfig():
    log.info('Fetching SmartThings config')
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
        return secret
