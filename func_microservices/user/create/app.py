import os
import requests
import json
import ast
from util import request_update,cont_or_serv_remove_logic

swarm = ast.literal_eval(os.environ['SWARM'])
db_manager_url = os.environ['DB_MANAGER_URL']
dbm_api_urls = ast.literal_eval(os.environ['DBM_API_URLS'])
faas_manager_url = os.environ['FAAS_MANAGER_URL']
faas_api_urls = ast.literal_eval(os.environ['FAAS_API_URLS'])
status_codes = ast.literal_eval(os.environ['STATUS_CODES'])
cont_or_serv_name = os.environ['CONT_OR_SERV_NAME']
request_id = os.environ['REQUEST_ID']
request_type = os.environ['REQUEST_TYPE']
user_name = os.environ['USER_NAME']
password = os.environ['PASSWORD']

request_data ={
    "db_manager_url" : db_manager_url,
    "api_url" : dbm_api_urls["request"]["update"],
    "request_id" : request_id,
    "request_type" : request_type
}

faas_manager_data ={
    "faas_manager_url" : faas_manager_url,
    "faas_api_urls" : faas_api_urls,
    "cont_or_serv_name" : cont_or_serv_name
}

def user_create(user_name, password):
    user_name = user_name
    required_url = db_manager_url + dbm_api_urls["user"]["create"]
    data = {
        "userName": user_name,
        "password": password
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    request_obj = requests.post(required_url, data = json.dumps(data), headers = headers)

    if request_obj.status_code == 201:
        request_obj_json = request_obj.json()
        data = {
            "userId": request_obj_json["userId"],
            "userName": user_name,
            "requestStatus": "User Created - Your userId is " + request_obj_json["userId"],
            "result": "success"
        }
    elif request_obj.status_code == 400:
        data = {
            "userId": None,
            "userName": user_name,
            "requestStatus": "User Creation Failed - User Name Already Taken",
            "result": "failure"
        }
    else:
        data = {
            "userId": None,
            "userName": user_name,
            "requestStatus": "User Creation Failed - " + str(request_obj.text),
            "result": "failure"
        }
    return data

if __name__ == "__main__":
    container_started_update = request_update(request_data,status_codes[request_type][102], "in_progress")
    if container_started_update:
        response_data = user_create(user_name, password)
        request_update(request_data, response_data["requestStatus"], response_data["result"])
        cont_or_serv_remove_logic( swarm , faas_manager_data)
    else:
        raise Exception("Fatal Exception - Request Update Failed")
