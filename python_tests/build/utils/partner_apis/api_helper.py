from basicauth import decode

import requests
import hashlib
from datetime import datetime, date, time, timezone, timedelta
import hmac
import re
import os
from hmac import HMAC
import http
import json
from database_connections import organizations
from utils.config_setup import config
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry, MaxRetryError

SECRET = "AD4LZnwgUwaLGF6PQbyNr3cTNABrsYts"
LOOKUP_CODE = "sB9sMZXUNEdRdJA73WuemU3YKJgXRr3D"


def _initiate_api_call_as_smoke_broker(org_name, json_body=None,
                                       timestamp=datetime.utcnow().isoformat()):
    info_dict = {"Body": [],
                 "Payload": []}
    org_code = organizations.get_org_code_by_name(org_name)
    secret_bytes = bytes(SECRET, 'utf-8')
    message = f"logged_in_user=qa_ui_automation,organization_code={org_code},lookup_code={LOOKUP_CODE}," \
              f"date_time_string={timestamp}"
    message_bytes = bytes(message, 'utf-8')
    digest = hmac.new(secret_bytes, message_bytes, hashlib.sha256)
    signature = digest.hexdigest()
    if json_body:
        temp = json.dumps(json_body, indent=2)
        info_dict["Body"].append(re.sub("\n ", "", temp))
    else:
        info_dict["Body"].append("")
    info_dict["Payload"].append({"Signature": signature,
               "AuthenticationString": message,
               "Content-Type": "application/json",
               "Cache-Control": "no-cache"
               })
    return info_dict


def retry_api_requests():
    """This method will automagically retry the below failed response codes up to 4 times, with automatic sleeps
    example:
    r = retry_api_requests()
    r.get(url)
    """
    retry_strategy = Retry(
        total=4,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504, 403],
        method_whitelist=["PUT", "GET", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def request_as_smoke_broker(org_name, url, request_method, json_body=None):
    if request_method == "post":
        request_data = _initiate_api_call_as_smoke_broker(org_name, json_body,
                                                          timestamp=datetime.now(timezone.utc).astimezone().isoformat())
    else:
        request_data = _initiate_api_call_as_smoke_broker(org_name, json_body, datetime.utcnow().isoformat())

    body = request_data["Body"].pop()
    payload = request_data["Payload"].pop()
    api_request = retry_api_requests()

    if request_method == "post":
        try:
            response = api_request.post(url, data=body, headers=payload)
        except MaxRetryError:
            # reset the datetime and retry on silly ruby api failures with a ridiculous try catch
            _initiate_api_call_as_smoke_broker(org_name, json_body)
            payload = request_data["Payload"].pop()
            try:
                response = api_request.post(url, data=body, headers=payload)
            except MaxRetryError:
                response = requests.post(url, data=body, headers=payload)
                raise ValueError(response.json()["errors"][0]["message"])
    elif request_method == "put":
        response = api_request.put(url, data=body, headers=payload)
    elif request_method == "get":
        response = api_request.get(url, headers=payload)

    response_body = response.json()
    return response_body


# pass zip_code as list of  lat and lng
# for example zipcode=[28.5421015, -81.3725261]
# for lat and lng of a particular zipcode use site https://www.freemaptools.com
def find_a_provider_search_results(plan_name, distance, state_code, dentist_name, zipcode):
    lat = zipcode[0]
    lng = zipcode[1]
    encoded_str = 'Basic QUZvY3dMV1c3SWljMEI0UmtGR01Yc3N1V0dYYmpwUmo6QkFlN0FFMmR6QTV1MUNHaw=='
    username, password = decode(encoded_str)
    print(username, password)
    query_params = {"grant_type": "client_credentials"}

    URL = config()['base_urls']['FAP_generate_credentials']
    r = requests.post(url=URL, params=query_params, auth=(username, password))
    data = r.json()

    url = config()['base_urls']['FAP_guardian_search_results']
    payload = {"planName": plan_name,
               "lat": lat,
               "lng": lng,
               "distance": distance,
               "stateCode": state_code,
               "numberOfProviders": 100,
               "dentistName": dentist_name
               }
    headers = {'Authorization': f'Bearer {data["access_token"]}'}

    response = requests.post(url=url, data=payload, headers=headers)
    response_body = response.json()
    return response_body