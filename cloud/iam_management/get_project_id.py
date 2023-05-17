import requests
from cloud.region_configuration.region_config import Service

url = f"{''.join(Service.iam.endpoints)}/v3/auth/projects"

"""
Функция возвращает словарь проектов, который хранит ключ{имя проекта}: значение{id проекта}  
"""


def get_project_id(iam_token):
    header = {
        "Content-Type": "application/json;charset=utf8",
        "X-Auth-Token": str(iam_token)
    }
    data = {}
    response = requests.get(url, headers=header, data=data).json()
    projects_id = {}
    for i in range(0, len(response['projects'])):
        projects_id[response['projects'][i]['name']] = response['projects'][i]['id']
    print("projects_id added")
    return projects_id
