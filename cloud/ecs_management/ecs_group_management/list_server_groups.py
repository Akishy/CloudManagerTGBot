import requests
from cloud.region_configuration.region_config import Service

def list_server_groups(x_auth: str, project_id: str):
    url = f"{''.join(Service.ecs.endpoints)}/v2.1/{project_id}/os-server-groups"
    header = {
        "Content-Type": "application/json;charset=utf8",
        "X-Auth-Token": x_auth
    }
    # data = {}
    response = requests.get(url, headers=header, params=project_id).json()
    return response
