import json
from functools import wraps


def extra_stuff(some_function):
    @wraps(some_function)
    def wrapper(*args, **kwargs):
        print('before wrapped function called')
        original_response = some_function(*args, **kwargs)
        massaged_response = original_response
        print('after wrapped function called')
        return massaged_response

    return wrapper


@extra_stuff
def lambda_handler(event, context):
    return {'statusCode': 200}

if __name__ == '__main__':
    print(json.dumps(lambda_handler(None, None), indent=2))
