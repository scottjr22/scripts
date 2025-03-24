import os
import sys
import json

sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__)), "/home/pauls/deltarisk/backend/src"))

from accommon.config_manager import conf_man
# from accommon.config_manager import conf_man


def load_aerss_config_details_table(podid):
    """ Pulls all cmid's and updates each config type in aerss-config-details table using aerss-config-details lambda"""
    conf_man.aws_session(profile=podid)
    session = conf_man.aws_session()
    lambda_client = session.client("lambda")
    aerss_config_details_table = session.resource("dynamodb").Table("aerss-config-details-table")
    resp = lambda_client.invoke(FunctionName="aerss-list-devices", Payload="", InvocationType="RequestResponse")
    resp = json.loads(resp["Payload"].read().decode("utf-8"))
    # print(resp)
    idx = 0
    for device in resp:
        idx +=1
        cmid = device.get("client_module_id")
        print(cmid)
        payload = { "client_module_id": cmid,
                   "config_type": "internal_config",
                   "action": "update"}
        payload = json.dumps(payload)
        resp = lambda_client.invoke(FunctionName="aerss-config-details", Payload=payload, InvocationType="RequestResponse")
        resp = json.loads(resp["Payload"].read().decode("utf-8"))
        print(resp)

        # Check if entry exists, if not create one
        resp = aerss_config_details_table.get_item(Key={"client_module_id": cmid})
        if not resp.get("Item"):
            #insert it
            print(f'{resp=} for {cmid=}')
            aerss_config_details_table.update_item(Key={"client_module_id": cmid})



if __name__ == "__main__":
    load_aerss_config_details_table("lion")
