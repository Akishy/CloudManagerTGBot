"""
Used to obtain a user token through username/password-based authentication.
"""
import json

from region_config import service, region, account, domain
import requests

url = f"https://{service.iam}.{region.endpoint}/v3/auth/tokens"

account.user_name = "bogdanov"
account.password = "q987654321wW"
domain.domain_name = "ADV-f4b56b47d226490f8c12"

payload = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "name": account.user_name,
                        "password": account.password,
                        "domain": {
                            "name": domain.domain_name
                        }
                    }
                }
            },
            "scope": {
                "project": {
                    "name": region.region_ID
                }
            }
        }
    }
response = requests.post(url, json=payload)

with open('new_file.json', 'w') as f:
    f.writelines(str(json.dumps(json.loads(response.content), indent=4, sort_keys=True)))
    f.close()

with open('obtained_token.json', 'w') as f:
    f.writelines(str(json.dumps(dict(response.headers), indent=4, sort_keys=True)))
    f.close()


