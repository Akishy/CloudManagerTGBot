"""
This file will contain the entire basic configuration for the cloud platform. Here the base classes for services
are defined, with the help of which the URI request will be formed, as well as a description of the region
"""

class service:
    iam = "iam"


class region:
    name = "RU-Moscow"
    region_ID = "ru-moscow-1"
    endpoint = f"{region_ID}.hc.sbercloud.ru"


class region_info:
    region_id = str


# This info can be found un "my credentials"
class account:
    user_name = str  # IAM User Name
    user_id = str  # IAM User ID
    password = str


class domain:
    domain_name = str  # Account Name
    domain_id = str  # Account ID


class project:
    project_id = str
    project_name = str


class user_group:
    name = str
    id = str  # Group ID


class agency_info:  # TODO
    agency = str
