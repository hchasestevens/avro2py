import requests
import re
import sys

cloud_repo_username = sys.argv[1]
cloud_repo_password = sys.argv[2]
new_version = sys.argv[3]


def validate_new_version():
    package_name = "avro2py"
    if new_version in get_versions_from_cloud_repo(package_name):
        raise Exception(
            """The specified version of this library (%s) already exists in CloudRepo. Increment the 
            version in the setup.py file """ % new_version
        )


def get_versions_from_cloud_repo(package_name):
    url = "https://teikametrics.mycloudrepo.io/repositories/teika-pypi/%s" % package_name
    data = requests.get(url, auth=(cloud_repo_username, cloud_repo_password)).content
    return set(re.findall("avro2py-(.*?)\.tar", str(data)))


validate_new_version()
