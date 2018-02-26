import boto3
import logging
from bson import json_util
import json

REGION_NAME = 'us-west-2'
PIPELINE_NAME = 'simple-pipeline-dev'
STAGE_NAME = 'DeploymentApproval'
ACTION_NAME = 'Approval'


def get_api_client(aws_service):
    try:
        api_session = boto3.Session(region_name=REGION_NAME)
        api_client = api_session.client(aws_service)
        return api_client
    except Exception as x:
        logging.error('Exception caught in get_api_client(): {}'.format(x))
        return None


def lambda_handler(event, context):
    try:
        pipeline_client = get_api_client('codepipeline')
        response = pipeline_client.get_pipeline_state(name=PIPELINE_NAME)

        token = None
        for stage in response.get('stageStates', []):
            stage_name = stage.get('stageName', None)
            if stage_name == STAGE_NAME:
                for action_state in stage.get('actionStates', []):
                    tmp = action_state.get('latestExecution', {}).get('token', None)
                    if tmp:
                        token = tmp
                        break

        print('token: {}'.format(token))

        if token:
            response = pipeline_client.put_approval_result(
                pipelineName=PIPELINE_NAME,
                stageName=STAGE_NAME,
                actionName=ACTION_NAME,
                result={
                    'summary': 'approved by approver',
                    'status': 'Approved'
                },
                token=token
            )

            print(json.dumps(response, indent=4, default=json_util.default))
            return True
        else:
            return False
    except Exception as x:
        logging.error('Exception caught in get_api_client(): {}'.format(x))
        return False

if __name__ == '__main__':
    lambda_handler(None, None)
