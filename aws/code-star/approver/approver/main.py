from utility import FlaskLambda
from utility import get_api_client
from flask import request
from bson import json_util
import json


'''
The FlaskLambda object that is created is the entry point for the lambda. The
LambdaTool deployer expects this to be called 'lambda_handler'
'''
lambda_handler = FlaskLambda(__name__)

REGION_NAME = 'us-west-2'
PIPELINE_NAME = 'simple-pipeline-dev'
STAGE_NAME = 'DeploymentApproval'
ACTION_NAME = 'Approval'

bucket = 'cmrsol-xfer'
random_bytes = '5dbce472088bac28be1b2a2fd6c7166f'
s3_key = 'approver/{}/page.html'.format(random_bytes)
s3_client = get_api_client('s3')


@lambda_handler.route('/', methods=['GET'])
def document():
    '''
    Write the HTML for the SPA out the network pipe

    Args:
        None

    Returns:
        tuple of (body, status code, content type) that API Gateway understands
    '''
    print('/ called: {}'.format(s3_client))
    html = read_html()
    return (
        html,
        200,
        {'Content-Type': 'text/html'}
    )


@lambda_handler.route('/approval', methods=['POST'])
def food():
    '''
    A contrived example function that will return some meta-data about the
    invocation.

    Args:
        None

    Returns:
        tuple of (body, status code, content type) that API Gateway understands
    '''
    print('/approval posted: {}'.format(request.json))
    try:
        data = {
            'form': request.form.copy(),
            'args': request.args.copy(),
            'json': request.json
        }

        if data and 'message' in request.json and 'approval_status' in request.json:
            message = request.json.get('message', 'no comment')
            approval_status = request.json.get('approval_status', False)
            r, http_code = put_approval_result(message, approval_status)
        else:
            data = {}
            http_code = 500
    except Exception as wtf:
        print('error: /approval caught - {}'.formnat(wtf))
        data = {}
        http_code = 500

    return (
        json.dumps(data),
        http_code,
        {'Content-Type': 'application/json'}
    )


def read_html():
    print('read_html() called: {}'.format(s3_client))
    the_bits = None
    try:
        print('read_html() calling get_object({}, {}): '.format(bucket, s3_key))
        s3_file = s3_client.get_object(
            Bucket=bucket,
            Key=s3_key
        )
        the_bits = s3_file['Body'].read()
        print('read_html() called get_object(}')
    except Exception as confusion:
        print('Exception caught in read_html(): {}'.format(confusion))

    return the_bits


def put_approval_result(notes, approval):
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
            if approval:
                status = 'Approved'
            else:
                status = 'Rejected'

            response = pipeline_client.put_approval_result(
                pipelineName=PIPELINE_NAME,
                stageName=STAGE_NAME,
                actionName=ACTION_NAME,
                result={
                    'summary': notes,
                    'status': status
                },
                token=token
            )

            print(json.dumps(response, indent=4, default=json_util.default))
            return True, 201
        else:
            return False, 400
    except Exception as x:
        print('error: exception caught in get_api_client(): {}'.format(x))
        return False, 500


if __name__ == '__main__':
    lambda_handler.run(debug=True)
