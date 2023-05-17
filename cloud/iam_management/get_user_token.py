# coding: utf-8

import json
import requests
from cloud.region_configuration.region_config import Service, Region, Domain
from huaweicloudsdkcore.exceptions import exceptions

"""
object.content_type = object['Content-Type']
object.content_length = dict['Content-length']
connection = dict['Connection']
date = dict['Date']
x_iam_trace_id = dict['X-IAM-Trace-Id']
cache_control = dict['Cache-Control']
pragma = dict['Pragma']
expires_on = dict['Expires']
auth_token = dict['X-Subject-Token']
x_request_id = dict['X-Request-Id']
x_frame_options = dict['X-Frame-Options']
x_content_type_options = dict['X-Content-Type-Options']
x_download_options = dict['X-Download-Options']
x_xss_protection = dict['X-XSS-Protection']
"""


def get_user_token(user_name: str, domain_name: str, passw: str):
    url = f"{''.join(Service.iam.endpoints)}/v3/auth/tokens"
    Domain.domain_name = domain_name
    try:
        request = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": user_name,
                            "password": passw,
                            "domain": {
                                "name": domain_name
                            }
                        }
                    }
                },
                "scope": {
                    "project": {
                        "name": Region.region_ID
                    }
                }
            }
        }
        response = requests.post(url, json=request)
        if response.status_code == 201:
            print(response.status_code, " -- The creation is successful.")
        else:
            print(response.status_code, response.text)
        return json.loads(json.dumps(dict(response.headers))), response.status_code
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)