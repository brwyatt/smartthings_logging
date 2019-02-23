import boto3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

import smartthings_logging.kms as kms


def getKey(bucket, filename):
    s3 = boto3.client('s3', region_name='us-west-2')
    ciphertext = s3.get_object(
        Bucket=bucket,
        Key=filename
    )['Body'].read()

    plaintext = kms.decrypt(ciphertext)

    return plaintext


def getConfig(bucket, filename):
    s3 = boto3.client('s3', region_name='us-west-2')

    key = getKey(bucket, filename+'.key')

    ciphertext = s3.get_object(
        Bucket=bucket,
        Key=filename
    )['Body'].read()

    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    return str(remove_padding(
        decryptor.update(ciphertext) + decryptor.finalize()), 'utf-8')


def pad(plaintext, blocksize=16):
    if type(plaintext) is not bytes:
        if type(plaintext) is str:
            plaintext = bytes(plaintext, 'utf-8')
        else:
            plaintext = bytes(plaintext)

    length = 16 - (len(plaintext) % 16)
    plaintext += bytes([length])*length

    return plaintext


def remove_padding(plaintext):
    return plaintext[:-plaintext[-1]]
