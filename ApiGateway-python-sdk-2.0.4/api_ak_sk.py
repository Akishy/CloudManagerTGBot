from typing import TYPE_CHECKING
from apig_sdk import signer

import requests
import json


def call_wrapper(access_key, secret_key, method, uri, xdomainid, project, request_content_file):
    """
    Calls SberCloud.Advanced API and signs the request with AK/SK
    Inputs:
        - access_key: Access Key, string
        - secret_key: Secret Key, string
        - method: REST method that will be executed. Most often it will be GET or POST, string
        - uri: request URI is in the following format: {URI-scheme}://{Endpoint}/{resource-path}?{query-string}, string. For example, https://ecs.ru-moscow-1.hc.sbercloud.ru/v1/{project_id}/cloudservers
        - xdomainid: X-Domain-Id of the root account (required for some IAM-related services), string
        - request_content_file: name of the file, which contains request body in JSON format, string
    Outputs:
        - none
    """

    # Initialize HuaweiCloud signer
    sig = signer.Signer()

    # Assign AK and SK
    sig.Key = access_key
    sig.Secret = secret_key

    # Read request from file and prepare the request body
    request_body = ""

    # В случае, если получен файл (.json), то его содержимое становится телом будущего запроса
    if request_content_file:
        with open(request_content_file) as jsonfile:
            js = json.load(jsonfile)

        # Переменная для хранения тела запроса (из .json)
        request_body = json.dumps(js)

    # Construct request
    if xdomainid:
        request = signer.HttpRequest(method, uri, {"Content-Type": "application/json", "X-Domain-Id": xdomainid}, request_body)
    elif project:
        request = signer.HttpRequest(method, uri, {"Content-Type": "application/json", "X-Project-Id": project}, request_body)
    else:
        request = signer.HttpRequest(method, uri, {"Content-Type": "application/json"}, request_body)

    # Sign request
    sig.Sign(request)

    # Execute request and print results
    resp = requests.request(request.method, request.scheme + "://" + request.host + request.uri, headers=request.headers, data=request.body)
    print(resp.status_code)
    resp.close()
    print(json.dumps(resp.json()))

    return True


# Пример использования 
call_wrapper('IPVWDPGG8VJI6ARZL98K', 'snYCdpJSr3rTZNkm7w8eaqyEPGn5X2byBJavjP5X', 'GET', 'https://vpc.ru-moscow-1.hc.sbercloud.ru/v1/e674f689c85a460dbbac7928547de1ac/vpcs', None, None, None)
