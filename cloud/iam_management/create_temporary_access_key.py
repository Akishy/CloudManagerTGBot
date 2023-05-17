import requests
from cloud.region_configuration.region_config import Service, AccessKey

"""
How to use:
Вызвать функцию, в первый параметр вставить юзер токен, во второй время жизни ключа доступа в секундах (минимально 900 сек, 15 минут)
функция возвращает json в формате словаря python. Из него можно доставать нужные данные.temp_access_key.access
var.access - AK
var.expires_at - когда истекает 
var.secret - SK
var.securitytoken - секурититокен
"""


def create_temporary_access_key(iam_token, time_to_live_sec):
    url = f"{''.join(Service.iam.endpoints)}/v3.0/OS-CREDENTIAL/securitytokens"

    header = {
        "Content-Type": "application/json;charset=utf8",
        "X-Auth-Token": str(iam_token)
    }
    payload = {
        "auth": {
            "identity": {
                "methods": [
                    "token"
                ],
                "token": {
                    "duration_seconds": int(time_to_live_sec)
                }
            }
        }
    }

    response = requests.post(url, data=str(payload), headers=header).json()
    response = AccessKey(response['credential'])
    return response
