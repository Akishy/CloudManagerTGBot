"""
This file will contain the entire basic configuration for the cloud platform. Here the base classes for services
are defined, with the help of which the URI request will be formed, as well as a description of the region
"""
from huaweicloudsdkcore.region.region import Region


class Service:
    iam = Region("ru-moscow-1", "https://iam.ru-moscow-1.hc.sbercloud.ru")
    ims = Region("ru-moscow-1", "https://ims.ru-moscow-1.hc.sbercloud.ru")
    ecs = Region("ru-moscow-1", "https://ecs.ru-moscow-1.hc.sbercloud.ru")
    vpc = Region("ru-moscow-1", "https://vpc.ru-moscow-1.hc.sbercloud.ru")

# This info can be found on "my credentials"
class User():
    def __init__(self, name, id, password):
        self.iam_user_name = name  # IAM User Name
        self.iam_user_id = id  # IAM User ID
        self.password = password


class Region(object):
    region_ID = "ru-moscow-1"


class AccessKey(object):
    def __init__(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])


class Domain:
    domain_name = str  # Account Name
    domain_id = str  # Account ID


class Project:
    project_id = str
    project_name = str


class User_group:
    name = str
    id = str  # Group ID


class Agency_info:  # TODO
    agency = str
