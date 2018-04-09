from bson import json_util #noqa
import json #noqa
import boto3
import logging
from botocore.exceptions import ClientError
from utility import execute_command


NoSuchEntity = 'NoSuchEntity'
LimitExceeded = 'LimitExceeded'
development = True


class KeyTool:
    _iam_client = None
    _ssm_client = None
    _user_name = None
    _access_key = None
    _secret = None
    _existing_keys = None

    def __init__(self, user_name, profile):
        try:
            self._user_name = user_name
            if profile:
                api_session = boto3.Session(profile_name=profile)
            else:
                api_session = boto3.Session()

            self._iam_client = api_session.client('iam')
            self._ssm_client = api_session.client('ssm')
        except Exception as x:
            logging.error('Exception caught in initialization(): {}'.format(x))
            return None

    def _list_access_keys(self):
        try:
            self._existing_keys = []
            r = self._iam_client.list_access_keys(UserName=self._user_name)
            key_data = r.get('AccessKeyMetadata', [])
            for k in key_data:
                wrk = k.get('AccessKeyId', None)
                if wrk:
                    self._existing_keys.append(wrk)
            print(json.dumps(self._existing_keys, indent=2, default=json_util.default))
            return True
        except ClientError as x:
            error_code = x.response['Error']['Code']
            if error_code == NoSuchEntity:
                print('list_access_keys() user not found')
            elif error_code == LimitExceeded:
                print('list_access_keys() access key limit reached')
            else:
                print('list_access_keys() strange error: {}'.format(error_code))
        except Exception as wtf:
            print('list_access_keys() exploded [{}]: {}'.format(type(wtf), wtf))

        return False

    def _create_credentials(self):
        print('Setting creds for {}'.format(self._user_name))
        try:
            r = self._iam_client.create_access_key(UserName=self._user_name)
            self._access_key = r.get('AccessKey', {}).get('AccessKeyId', None)
            self._secret = r.get('AccessKey', {}).get('SecretAccessKey', None)
            if self._access_key and self._secret:
                print('Access key generated')
                return True
            else:
                print('Access key NOT generated')
        except ClientError as x:
            error_code = x.response['Error']['Code']
            if error_code == NoSuchEntity:
                print('create_credentials() user not found')
            elif error_code == LimitExceeded:
                print('create_credentials() access key limit reached')
            else:
                print('create_credentials() strange error: {}'.format(error_code))
        except Exception as wtf:
            print('create_credentials() exploded [{}]: {}'.format(type(wtf), wtf))

        return False

    def _store_credentials(self):
        print('Storing creds to SSM')
        try:
            access_key_key = '/service_account/{}/access_key'.format(self._user_name)
            secret_key = '/service_account/{}/secret'.format(self._user_name)
            r = self._ssm_client.put_parameter( # noqa
                    Name=access_key_key,
                    Value=self._access_key,
                    Type='SecureString',
                    Overwrite=True
            )
            print('Access key stored in {}'.format(access_key_key))

            r = self._ssm_client.put_parameter( # noqa
                    Name=secret_key,
                    Value=self._secret,
                    Type='SecureString',
                    Overwrite=True
            )
            print('Secret stored in {}'.format(secret_key))

            return True
        except Exception as wtf:
            print('store_credentials() exploded [{}]: {}'.format(type(wtf), wtf))

        return False

    def _delete_existing_keys(self):
        # import pdb; pdb.set_trace()
        try:
            tmp_client = boto3.client( #noqa
                'iam',
                aws_access_key_id=self._access_key,
                aws_secret_access_key=self._secret,
                aws_session_token='SESSION_TOKEN'
            )

            command = ['aws', 'configure', 'set', 'aws_access_key_id', self._access_key]
            r, out, err = execute_command(command)
            if r > 0:
                return False

            command = ['aws', 'configure', 'set', 'aws_secret_access_key', self._secret]
            r, out, err = execute_command(command)
            if r > 0:
                return False

            for key in self._existing_keys:
                response = self._iam_client.delete_access_key( #noqa
                    UserName=self._user_name,
                    AccessKeyId=key
                )
                print(json.dumps(response, indent=2, default=json_util.default))

            return True
        except ClientError as x:
            error_code = x.response['Error']['Code']
            print('delete_existing_keys() strange error: {}'.format(error_code))
        except Exception as wtf:
            print('delete_existing_keys() exploded [{}]: {}'.format(type(wtf), wtf))

        return False

    def rotate_key(self):
        if not self._list_access_keys():
            return False

        status = self._create_credentials()
        if not status:
            return False

        status = self._store_credentials()
        if not status:
            return False

        status = self._delete_existing_keys()

        if development:
            return True

        return status
