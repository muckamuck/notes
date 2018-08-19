import json
import os
import sys
import traceback
import boto3


region = os.environ.get('sqs_region', 'us-east-1')
verbose = False
sqs_client = boto3.client('sqs', region_name=region)


try:
    q_url = sys.argv[1]
    print('q_url: {}'.format(q_url))
except Exception as x:
    print('usage: python {} <queue-url>'.format(sys.argv[0]))
    sys.exit(1)


def receive_message():
    stop = False
    while not stop:
        try:
            message_count = 0
            r = sqs_client.receive_message(
                QueueUrl=q_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20
            )

            for m in r.get('Messages', []):
                _body = m.get('Body', None)
                if _body == 'stop':
                    stop = True

                try:
                    body = json.loads(_body)
                    print(json.dumps(body, indent=2))
                except:
                    print(_body)

                receipt_handle = m.get('ReceiptHandle', None)
                sqs_client.delete_message(
                        QueueUrl=q_url,
                        ReceiptHandle=receipt_handle
                )
                message_count = message_count + 1

            print('processed {} messages'.format(message_count))
            if verbose:
                print('receive_message() response: {}'.format(json.dumps(r, indent=2)))
        except Exception as wtf:
            print('submit_job() exploded: {}'.format(wtf))
            traceback.print_exc(file=sys.stdout)
            return False


if __name__ == '__main__':
    receive_message()
