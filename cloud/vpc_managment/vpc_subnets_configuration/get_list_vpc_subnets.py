from cloud.region_configuration.region_config import Service
import requests
from pydantic import BaseModel, ValidationError
from uuid import UUID
from ipaddress import IPv4Network, IPv4Address
import json


# class DNS(BaseModel):



class Subnet(BaseModel):
    id: UUID
    name: str
    description: str
    cidr: IPv4Network
    dnsList: list[IPv4Address]
    status: str
    scope: str
    vpc_id: UUID
    ipv6_enable: bool
    gateway_ip: IPv4Address
    dhcp_enable: bool
    primary_dns: IPv4Address
    secondary_dns: IPv4Address
    availability_zone: str
    neutron_network_id: UUID
    neutron_subnet_id: UUID
    extra_dhcp_opts: list


class Subnets(BaseModel):
    subnets: list[Subnet]



def get_list_vpc_subnets(x_auth, project_id, vpc_id):
    url = f"{''.join(Service.vpc.endpoints)}/v1/{project_id}/subnets"
    header = {
        "Content-Type": "application/json;charset=utf8",
        "X-Auth-Token": str(x_auth)
    }

    response = requests.get(url=url, headers=header, params={"vpc_id":vpc_id}).json()
    try:
        response = Subnets.parse_raw(json.dumps(response))
        return response
    except ValidationError as e:
        print(e.json())