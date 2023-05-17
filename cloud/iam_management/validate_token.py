from __future__ import annotations

import requests
import json
from cloud.region_configuration.region_config import Service
from typing import List
from pydantic import BaseModel, ValidationError


class Endpoint(BaseModel):
    id: str
    interface: str
    region: str
    region_id: str
    url: str


class CatalogItem(BaseModel):
    endpoints: List[Endpoint]
    id: str
    name: str
    type: str


class Domain(BaseModel):
    id: str
    name: str
    xdomain_id: str
    xdomain_type: str


class Project(BaseModel):
    domain: Domain
    id: str
    name: str


class Role(BaseModel):
    id: str
    name: str


class Domain1(BaseModel):
    id: str
    name: str
    xdomain_id: str
    xdomain_type: str


class User(BaseModel):
    domain: Domain1
    id: str
    name: str
    password_expires_at: str


class Token(BaseModel):
    catalog: List[CatalogItem]
    expires_at: str
    issued_at: str
    methods: List[str]
    project: Project
    roles: List[Role]
    user: User


class Model(BaseModel):
    token: Token


def validate_token(x_auth_verification_token, x_subject_token_to_validate):
    url = f"{''.join(Service.iam.endpoints)}/v3/auth/tokens"
    header = {
        "Content-Type": "application/json;charset=utf8",
        "X-Auth-Token": x_auth_verification_token,
        "X-Subject-Token": x_subject_token_to_validate
    }

    response = requests.get(url, headers=header).status_code
    return response
    # try:
    #     response = Model.parse_raw(json.dumps(response))
    #     return response
    # except ValidationError as e:
    #     print(e.json())