from bson import json_util #noqa
import json #noqa
import boto3
import sys
import logging
from botocore.exceptions import ClientError


NoSuchEntity = 'NoSuchEntity'
LimitExceeded = 'LimitExceeded'


def print_usage():
    print('usage: python {} <user-name>'.format(sys.argv[0]))


def get_api_client(aws_service):
    '''
    Get an AWS client

    Args:
        None

    Returns:
        AWS client connection | None
    '''
    try:
        api_session = boto3.Session()
        api_client = api_session.client(aws_service)
        return api_client
    except Exception as x:
        logging.error('Exception caught in get_api_client(): {}'.format(x))
        return None


def list_access_keys(user):
    pass


def create_credentials(user):
    print('Setting creds for {}'.format(user))
    try:
        iam_client = get_api_client('iam')
        r = iam_client.create_access_key(UserName=user)
        access_key = r.get('AccessKey', {}).get('AccessKeyId', None)
        secret = r.get('AccessKey', {}).get('SecretAccessKey', None)
        if access_key and secret:
            print('Access key generated')
            return access_key, secret
        else:
            print('Access key NOT generated')
    except ClientError as x:
        error_code = x.response['Error']['Code']
        if error_code == NoSuchEntity:
            print('set_credentials() user not found')
        elif error_code == LimitExceeded:
            print('set_credentials() access key limit reached')
        else:
            print('set_credentials() strange error: {}'.format(error_code))
    except Exception as wtf:
        print('set_credentials() exploded [{}]: {}'.format(type(wtf), wtf))

    return None, None


def store_credentials(user, access_key, secret):
    print('Storing creds to SSM')
    try:
        ssm_client = get_api_client('ssm')
        access_key_key = '/service_account/{}/access_key'.format(user)
        secret_key = '/service_account/{}/secret'.format(user)
        r = ssm_client.put_parameter( # noqa
                Name=access_key_key,
                Value=access_key,
                Type='SecureString',
                Overwrite=True
        )
        print('Access key stored in {}'.format(access_key_key))

        r = ssm_client.put_parameter( # noqa
                Name=secret_key,
                Value=secret,
                Type='SecureString',
                Overwrite=True
        )
        print('Secret stored in {}'.format(secret_key))

        return True
    except Exception as wtf:
        print('store_credentials() exploded [{}]: {}'.format(type(wtf), wtf))

    return False


def delete_existing_keys(existing_keys):
    pass


if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] == '-?' or sys.argv[1] == '--help':
        print_usage()
        sys.exit(1)

    user_name = sys.argv[1]
    status, existing_keys = list_access_keys(user_name)

    if status:
        status, access_key, secret = create_credentials(user_name)
    else:
        sys.exit(1)

    if status:
        status = store_credentials(sys.argv[1], access_key, secret)
    else:
        sys.exit(1)

    if status:
        status = delete_existing_keys(existing_keys)
    else:
        sys.exit(1)

    if status:
        sys.exit(0)
    else:
        sys.exit(1)
