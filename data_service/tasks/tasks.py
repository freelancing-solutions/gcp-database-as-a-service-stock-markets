from google.cloud import tasks_v2
from google.protobuf.timestamp_pb2 import Timestamp
import datetime
import json

queue = "default-queue"
location = "us-central1"
project = "pinoydesk"


def create_task(uri, payload, in_seconds):
    # Create a client.
    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(project, location, queue)

    # Construct the request body.
    task = {
        'app_engine_http_request': {  # Specify the type of request.
            'http_method': tasks_v2.HttpMethod.POST,
            'relative_uri': uri
        }
    }
    if payload is not None:
        if isinstance(payload, dict):
            # Convert dict to JSON string
            payload = json.dumps(payload)
            # specify http content-type to application/json
            task["app_engine_http_request"]["headers"] = {"Content-type": "application/json"}
        # The API expects a payload of type bytes.
        converted_payload = payload.encode()

        # Add the payload to the request.
        task['app_engine_http_request']['body'] = converted_payload

    if in_seconds is not None:
        # Convert "seconds from now" into an rfc3339 datetime string.
        schedule_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=in_seconds)
        timestamp = Timestamp().FromDatetime(schedule_time)

        # Add the timestamp to the tasks.
        task['schedule_time'] = timestamp

    # Use the client to build and send the task.
    # noinspection PyTypeChecker,PyBroadException
    try:
        # noinspection PyTypeChecker
        response = client.create_task(parent=parent, task=task)
    except Exception as e:
        return None
    return response
