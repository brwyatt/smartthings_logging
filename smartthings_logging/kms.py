import boto3


def decrypt(ciphertext):
    kms = boto3.client('kms', region_name='us-west-2')

    return kms.decrypt(CiphertextBlob=ciphertext)['Plaintext']
