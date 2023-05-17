import requests
from cloud.region_configuration.region_config import Service

url = f"{''.join(Service.iam.endpoints)}/v3/auth/domains"

"""
Функция возвращает словарь, в котором информация об аккаунте в таком порядке: ключ[имя аккаунта] = значение[id_аккаунта]
"""


def get_account_info(iam_token):
    header = {
        "Content-Type": "application/json;charset=utf8",
        "X-Auth-Token": str(iam_token)
    }
    data = {}
    response = requests.get(url, headers=header, data=data).json()
    account_info = {}
    for i in range(0, len(response['domains'])):
        account_info[response['domains'][i]['name']] = response['domains'][i]['id']
    print("account info added")
    return account_info
