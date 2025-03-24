import os
import sys
import json
import requests

sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__)), "/home/pauls/deltarisk/backend/src"))

import boto3

from accommon.config_manager import conf_man
from accommon import functions
from accommon.cloud_software_hub import CloudSoftwareHub


def fetch_device_details(csh, lsn):
    device_details = csh.get_csh_device_details(lsn)
    print(f"{device_details=}")
    # Make sure device is enabled
    if device_details.get("enabled") != True:
        enabled = device_details.get("enabled")
        print(f"Device is not enabled: {enabled}")
    # Get device_id
    device_id = device_details.get("_id")
    customerNumber = device_details.get("customerNumber")
    device_name = device_details.get("name")

    print(f"{device_id=}")
    print(f"{customerNumber=}")
    print(f"{device_name=}")
    return device_id, customerNumber, device_name


def create_new_device(new_csh_region, device_name, customerNumber, session):
    csh = CloudSoftwareHub(region=new_csh_region, session=session)
    new_lsn = csh.create_device(device_name, device_name, customerNumber)
    print(f"{new_lsn=}")
    new_details = csh.get_csh_device_details(new_lsn)
    print(f"{new_details=}")
    enabled = new_details.get("enabled")
    if not enabled:
        print(f"Device is not enabled: {enabled}")


def relocate(csh, device_id, new_csh_region):
    resp = csh.relocate(device_id, new_csh_region)
    print(f"{resp=}")



def check_new_details(new_csh_region, lsn):
    csh = CloudSoftwareHub(region=new_csh_region, session=session)
    new_details = csh.get_csh_device_details(lsn)
    print(f"{new_details=}")
    status = csh.check_device_status_bravo("6793d19a6e7770cd4a43ec10")
    print(status)






if __name__ == "__main__":
    """
    event = {
        "lsn": "csh-aersscom-06c389288c94453df9df2fad04a0dbf8ce6ea645",
        "new_csh_region": "stagegov"
        "current_csh_region": "stagecom"
    }
    """

    # new_csh_region = "stagegov"
    # current_csh_region = "stagecom"
    # lsn = "csh-aersscom-06c389288c94453df9df2fad04a0dbf8ce6ea645" # This is Vetting SUS Lab
    # lsn = "csh-aersscom-1d80e66be9251fbb935f981587255232be6d9336" # This is VM
    # lsn = "csh-aersscom-migrationtest2" # This is non VM

    session = conf_man.aws_session()
    print(conf_man.get_config("aws_region"))
    print(conf_man.get_config("pod_id"))

    # Get Device Details from current CSH region
    creds = CloudSoftwareHub.get_csh_config("prodgov", "mapi/csh", session)
    csh = CloudSoftwareHub(config=creds, region="prodgov", session=session)


    # device_id, customerNumber, device_name = fetch_device_details(csh, lsn)
    # create_new_device(new_csh_region, device_name, customerNumber, session)
    # relocate(csh, device_id, new_csh_region)
    # new_csh = CloudSoftwareHub(region=new_csh_region, session=session)
    # resp = new_csh.check_relocate_status(device_id)
    # print(f"{resp=}")
    # payload = {
    #     "enabled": False,
    # }
    headers = {
        "Content-Type": "application/json",
        "authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6InNpZ25pbmdrZXkyMDI1IiwieDV0IjoiajVETUNXcFM4ejVjTVEtdm56Y0lSMC1jOGtRIiwicGkuYXRtIjoiMSJ9.eyJzY29wZSI6WyJDU0giLCJHTE8tT0tUQS1BUFAtQ1NILUFFRlVOQ1RJT05TLUFETUlOLVVzZXJzIl0sImNsaWVudF9pZCI6ImFlcnNzX2FwaSIsImlzcyI6Imh0dHBzOi8vaWRtbWFzdGVyLmltdy5tb3Rvcm9sYXNvbHV0aW9ucy5jb206NDQzIiwiYXVkIjoiaWRtbWFzdGVyLmltdy5tb3Rvcm9sYXNvbHV0aW9ucy5jb20iLCJpYXQiOjE3MzgyNTEzODgsImp0aSI6ImZDMk9MTUlSVDFLMk1ucmYzR3dIM2siLCJleHAiOjE3MzgyNTg1ODh9.DX7lXDW_03qtmxQ9i4kEcIgIE1C4S_vn0vFYQFyRJOu35JY1ldQOxs-Z-VV1fjePtIuUY6SmBWh4xdqq21sVP7l4sllbpW0pruDmpykEVvY_GCAltV0ySpO54GXntw6WlENWdywZ_hXnIVraQH5EzJA7qFFvuM17RbdMHkjyvQ5JC_axauchs0_lV54x4qLO9CieBNWIQOLytqqP_uzBjeYmKnrQKjajeCDSHiIDo3uP07wcD8PbjolPxME_RgS86berFR5pO97cdcf0H0z14H1FXSkh4W4j9Qql8fGiGDsnnQPZu1Om-rVxc1rvfgi0BqH3gWzPoThwygPjbasnDQ",
        "msi-csh-api-version": "1.7.0"
    }
    # url = "https://stage.pi.cloudsoftwarehub.motorolasolutions.com/api/device/6792986637e4564b74f922da"
    url = "https://gov.cloudsoftwarehub.motorolasolutions.com/api"
    # resp = requests.request(method="PATCH", url=url, headers=headers, data=json.dumps(payload))
    # resp = csh.make_http_request("PATCH", url, headers=headers, data=json.dumps(payload))
    resp = csh.headers()
    print(f"{resp=}")
    resp = csh.create_device("paultest", "paultest", "0112")
    print(f"{resp=}")

    # check_new_details(new_csh_region, lsn)
