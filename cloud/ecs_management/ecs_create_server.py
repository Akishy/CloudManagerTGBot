from cloud.region_configuration.region_config import Service
import requests


def ecs_create_server(x_auth, project_id, image_ref, flavour_ref, name, vpcid, subnet_id, volumetype: str, disc_size):
    url = f"{''.join(Service.ecs.endpoints)}/v1.1/{project_id}/cloudservers"
    header = {
        "Content-Type": "application/json;charset=utf8",
        "X-Auth-Token": x_auth
    }
    payload = f"{{\"server\":{{\"imageRef\":\"{image_ref}\",\"flavorRef\":\"{flavour_ref}\",\"name\":\"{name}\",\"vpcid\":\"{vpcid}\",\"nics\":[{{\"subnet_id\":\"{subnet_id}\"}}],\"root_volume\":{{\"volumetype\":\"{volumetype}\"}},\"data_volumes\":[{{\"volumetype\":\"{volumetype}\",\"size\":{disc_size}}}]}}}}"
    response = requests.post(url, data=payload, headers=header)
    return response.json()
