import boto3
import os #noqa
from datetime import datetime
from price import prices

first_token = 'first_token'


def lambda_handler(event, context):
    total_cost = 0.0
    now = datetime.utcnow()
    running_count = 1
    next_token = first_token
    try:
        ec2_client = boto3.client('ec2', region_name='us-east-1')

        while next_token:
            if next_token == first_token:
                r = ec2_client.describe_instances()
            else:
                r = ec2_client.describe_instances(NextToken=next_token)

            next_token = r.get('NextToken', None)
            for reservation in r.get('Reservations', {}):
                for machine in reservation.get('Instances', []):
                    state = machine.get('State', {}).get('Name')
                    if state == 'running':
                        instance_type = machine.get('InstanceType', 'special')
                        launch_time = machine.get('LaunchTime', 'a long long time ago...')
                        launch_time = launch_time.replace(tzinfo=None)
                        tags = machine.get('Tags', [])
                        machine_name = 'unknown'
                        for tag in tags:
                            if tag['Key'] == 'Name':
                                machine_name = tag.get('Value', 'unknown')
                        uptime = now - launch_time
                        hours = uptime.total_seconds() / 3600
                        price_per_hour = prices.get(instance_type, 0)
                        extended_cost = hours * price_per_hour
                        total_cost = extended_cost + total_cost
                        id = machine.get('InstanceId', 'unknown')
                        extended_cost = '{0:.2f}'.format(extended_cost)
                        print('{} {} {} {} {}'.format(extended_cost, launch_time, instance_type, id, machine_name))
                        running_count = running_count + 1

            print('total_cost: ${0:.2f}'.format(total_cost))
    except Exception as wtf:
        print(wtf)


if __name__ == '__main__':
    lambda_handler({}, None)
