from utils.config_setup import config
from utils import api_helper


def create_employee_api_call(org_name, request_type, subscriber_id=None, json_body=None):

    if request_type == "new_subscriber":
        url = config()['base_urls']['api'] + "/admin/v2/subscriber"
        request_method = "post"
    elif request_type == "get_subscriber_information":
        url = config()['base_urls']['api'] + f"/admin/v2/subscriber/{subscriber_id}"
        request_method = "get"
    elif request_type == "update_subscriber_information":
        url = config()['base_urls']['api'] + f"/admin/v2/subscriber/{subscriber_id}"
        request_method = "put"
    elif request_type == "rehire_subscriber":
        url = config()['base_urls']['api'] + f"/admin/v2/subscriber/{subscriber_id}/rehire"
        request_method = "put"
    elif request_type == "terminate_subscriber":
        url = config()['base_urls']['api'] + f"/admin/v2/subscriber/{subscriber_id}/terminate"
        request_method = "put"
    elif request_type == "remove_subscriber":
        url = config()['base_urls']['api'] + f"/admin/v2/subscriber/{subscriber_id}/removal?removal_reason=CCPA"
        request_method = "put"

    response = api_helper.request_as_smoke_broker(org_name, url, request_method, json_body=json_body)
    if response['status'] == "failure":
        raise Exception(response["errors"][0]["message"])
    else:
        return response['data']


def create_dependent_api_call(org_name, subscriber_id, request_type, dependent_id=None, json_body=None):

    if request_type == "new_dependent":
        url = config()['base_urls']['api'] + f"/admin/v2/subscriber/{subscriber_id}/dependent?is_custom_id=false"
        request_method = "post"
    elif request_type == "get_dependent_information":
        url = config()['base_urls']['api'] + f"/admin/v2/subscriber/{subscriber_id}/dependent/{dependent_id}?is_custom_id=false"
        request_method = "get"
    elif request_type == "update_dependent_information":
        url = config()['base_urls']['api'] + f"/admin/v2/subscriber/{subscriber_id}/dependent/{dependent_id}?is_custom_id=false"
        request_method = "put"
    elif request_type == "deactivate_dependent":
        url = config()['base_urls']['api'] + f"/admin/v2/subscriber/{subscriber_id}/dependent/{dependent_id}/deactivate?is_custom_id=false"
        request_method = "put"
    elif request_type == "reactivate_dependent":
        url = config()['base_urls']['api'] + f"/admin/v2/subscriber/{subscriber_id}/dependent/{dependent_id}/reactivate?is_custom_id=false"
        request_method = "put"

    response = api_helper.request_as_smoke_broker(org_name, url, request_method, json_body=json_body)
    if response['status'] == "failure":
        raise Exception(response["errors"][0]["message"])
    else:
        return response['data']