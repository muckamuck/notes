import boto3
import json #noqa
import sys


def do_voo_doo():
    count = 0
    client = boto3.client('iam')
    next_token = 'first'
    try:
        while next_token:
            if next_token == 'first':
                r = client.list_policies(
                    OnlyAttached=True
                )
            else:
                r = client.list_policies(
                    OnlyAttached=True,
                    Marker=next_token
                )

            next_token = r.get('Marker', None)
            for policy in r.get('Policies', []):
                arn = policy.get('Arn', None)
                version = policy.get('DefaultVersionId', None)

                if arn and version:
                    if is_s3_superman(client, arn, version):
                        print(arn)
                        count = count + 1

        print('Policy count: {}'.format(count))
    except Exception as wtf:
        print(wtf)


def is_s3_superman(client, arn, version):
    try:
        r = client.get_policy_version(
            PolicyArn=arn,
            VersionId=version
        )
        document = r.get('PolicyVersion', {}).get('Document', None)
        for s in document.get('Statement', []):
            resource = s.get('Resource', 'unknown')
            effect = s.get('Effect', 'unknown')
            if 's3:*' in s.get('Action', []) and resource == '*' and effect == 'Allow':
                return True
    except Exception as wtf:
        print(wtf)
        sys.exit(1)

    return False


if __name__ == '__main__':
    do_voo_doo()
