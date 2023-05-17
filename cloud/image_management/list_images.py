import requests
import json
from cloud.region_configuration.region_config import Service
from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, ValidationError, Field
from uuid import UUID


class Image(BaseModel):
    checksum: str
    container_format: str
    created_at: Optional[datetime]
    disk_format: str
    file: str
    hw_vif_multiqueue_enabled: bool
    id: UUID
    max_ram: int = None
    min_disk: int
    min_ram: int
    name: str
    owner: str
    protected: bool
    schema_: str = Field(alias='schema')
    self: str
    size: int
    status: str
    tags: list
    updated_at: Optional[datetime]
    virtual_env_type: str
    virtual_size: Any
    visibility: str


class Images(BaseModel):
    images: list[Image]


url = f"{''.join(Service.ims.endpoints)}/v2/cloudimages"
date = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
"""
imagetype: GOLD BY DEFAULT

Public image: The value is gold.
Private image: The value is private.
Shared image: The value is shared.
Market image: The value is market.


__os_type LINUX BY DEFAULT
string	query	No	
Specifies the OS type. The value can be Linux, Windows, or Other.


__platform UBUNTU BY DEFAULT
string	query	No	
Specifies the image OS type. Specifies the image platform type. The value can be Windows, Ubuntu, RedHat, SUSE, CentOS, 
Debian, OpenSUSE, Oracle Linux, Fedora, Other, CoreOS, or EulerOS.

"""


def get_list_images(x_auth: str, image_type="gold", os_type="Linux", platform="Ubuntu"):
    if image_type != ("gold" or "private" or "shared" or "market"):
        print("image_type is incorrect! you should enter gold or private or shared or market")

    headers = {
        'X-Auth-Token': x_auth,
        'X-Sdk-Date': date,
    }
    response = requests.get(url, headers=headers,
                            params={'__imagetype': image_type, '__os_type': os_type, '__platform': platform}).json()
    try:
        r = Images.parse_raw(json.dumps(response))
        return r
    except ValidationError as e:
        print(e.json())

    #return json.dumps(response, indent=4, sort_keys=True)
