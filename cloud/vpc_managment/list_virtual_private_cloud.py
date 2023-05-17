from cloud.region_configuration.region_config import Service
import requests
from pydantic import BaseModel, ValidationError
from uuid import UUID
from ipaddress import IPv4Network
from datetime import datetime
import json

"""
Функция принимает 2 значения: IAM_token, и project_id, который до этого был выбран пользователем в течение диалога с ботом
Функция возвращает класс VPC's, который содержит список с доступными сетями. После выбора идентификатора сети, например, [0](первая сеть в списке), или [1] (вторая сеть в списке), появляется возможность работать с классом vpc. По умолчанию на платформе существует дефолт сеть
Пример:  print(virtual_private_clouds.vpcs[0].id) - Отображает id первой (дефолтной) сети
"""
class Route(BaseModel):
    destination: IPv4Network
    nexthop: str

class Vpc(BaseModel):
    id: UUID
    name: str
    description: str
    cidr: IPv4Network
    status: str
    routes: list[Route]
    enterprise_project_id: str | int
    tenant_id: str = None
    created_at: datetime = None
    updated_at: datetime = None


class Vpcs(BaseModel):
    vpcs: list[Vpc]


def list_virtual_private_cloud(iam_token: str, project_id: str):
    url = f"{''.join(Service.vpc.endpoints)}/v1/{project_id}/vpcs"
    header = {
        "Content-Type": "application/json;charset=utf8",
        "X-Auth-Token": str(iam_token)
    }
    response = requests.get(url, headers=header).json()
    try:
        response = Vpcs.parse_raw(json.dumps(response))
        return response
    except ValidationError as e:
        print(e.json())
