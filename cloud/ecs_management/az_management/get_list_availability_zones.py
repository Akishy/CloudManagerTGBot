import requests
import json
from pydantic import BaseModel, ValidationError, Field
from typing import Any
from cloud.region_configuration.region_config import Service


class AZ(BaseModel):
    hosts: Any
    zoneState: dict
    zoneName: str


class AZ_info(BaseModel):
    availabilityZoneInfo: list[AZ]


def get_list_availability_zones(x_auth: str, project_id: str):
    url = f"{''.join(Service.ecs.endpoints)}/v2.1/{project_id}/os-availability-zone"
    header = {
        "Content-Type": "application/json;charset=utf8",
        "X-Auth-Token": str(x_auth)
    }
    response = requests.get(url, headers=header).json()

    try:
        r = AZ_info.parse_raw(json.dumps(response))
        return r
    except ValidationError as e:
        print(e.json())
