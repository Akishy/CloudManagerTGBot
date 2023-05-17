import requests
from cloud.region_configuration.region_config import Service
import json
from typing import Dict
from pydantic import BaseModel, Field, ValidationError


class Extra_specs(BaseModel):
    cond_operation_az: str = Field(alias='cond:operation:az')
    cond_operation_status: str = Field(alias="cond:operation:status")


class Flavor(BaseModel):
    id: str
    name: str
    os_flavor_access_is_public: bool = Field(alias="os-flavor-access:is_public")
    os_extra_specs: Extra_specs


class ModelFlavor(BaseModel):
    flavors: list[Flavor]

"""
функция возвращает объект, содержащий все снимки в выбранном регионе
"""


def get_list_flavours(x_auth: str, project_id: str, availability_zone: str):
    url = f"{''.join(Service.ecs.endpoints)}/v1/{project_id}/cloudservers/flavors"
    header = {
        "Content-Type": "application/json;charset=utf8",
        "X-Auth-Token": x_auth,
        # "availability_zone": availability_zone
    }
    response = requests.get(url, headers=header, params={"availability_zone": availability_zone}).json()
    try:
        r = ModelFlavor.parse_raw(json.dumps(response))
        return r
    except ValidationError as e:
        print(e.json())
    # return json.dumps(response, indent=4, sort_keys=True)
