import requests
import json
from tabulate import *

def get_ticket():
    api_url = "https://sandboxapicem.cisco.com/api/v1/ticket"
    headers = {
        "content-type": "application/json",
        "X-Auth-Tocken": ticket
    }
    body_json = {
        "username": "devnetuser",
        "password": "Cisco123!"
    }
    resp = requests.post(api_url, json.dumps(body_json), headers=headers, verify=False)
    status = resp.status_code
    if resp.status_code != 200:
        raise Exception("Status code does not equal 200. Response text: " + resp.text)
    response_json = resp.json()
    serviceTicket = response_json["response"]["serviceTicket"] 
    print("The service ticket number is: ", serviceTicket)
    return serviceTicket

def print_hosts():
    api_url = "https://sandboxapicem.cisco.com/api/v1/host"
    ticket = get_ticket()
    headers = {
        "content-type": "application/json"
    }
    resp = requests.get(api_url, headers=headers, verify=False)
    if resp.status_code != 200:
        raise Exception("Status code does not equal 200. Response text: " + resp.text)
    response_json = resp.json()

    host_list = []
    i = 0
    for item in response_json["response"]:
        i+=1
        host = [
             i,
             item["hostType"],
             item["hostIp"] 
        ]
        host_list.append( host )
    table_header = ["Number", "Type", "IP"]
    print( tabulate(host_list, table_header) )

print_hosts()


