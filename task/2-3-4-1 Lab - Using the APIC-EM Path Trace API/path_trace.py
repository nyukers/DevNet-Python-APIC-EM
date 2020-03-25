import requests
import json
import time
from apic_em_functions_sol import *
from tabulate import *

requests.packages.urllib3.disable_warnings()

api_url = "https://SandBoxAPICEM.cisco.com/api/v1/flow-analysis"
ticket = get_ticket()
headers = {
    "content-type": "application/json",
    "X-Auth-Token": ticket
}

print("List of hosts on the network: ")
print_hosts()
print("List of devices on the network: ")
print_devices()

print("\n\n")

while True:
    s_ip = input("Please enter the source host IP address for the path trace: ")
    d_ip = input("Please enter the destination host IP address for the path trace: ")
    if s_ip != "" or d_ip != "":
        path_data = {
            "sourceIP": s_ip,
            "destIP": d_ip
        }
        print("Source IP address is: ",       path_data["sourceIP"])
        print("Destination IP address is: ",  path_data["destIP"])
        break
    else:
        print("\n\nYOU MUST ENTER IP ADDRESSES TO CONTINUE.\nUSE CTRL-C TO QUIT\n")
        continue

path = json.dumps(path_data)
resp = requests.post(api_url, path, headers=headers, verify=False)

resp_json = resp.json()
flowAnalysisId = resp_json["response"]["flowAnalysisId"]
print("FLOW ANALYSIS ID: ", flowAnalysisId)

check_url = api_url + "/" + flowAnalysisId
status = ""
checks = 1
while status != "COMPLETED":
    r = requests.get(check_url, headers=headers, verify=False)
    response_json = r.json()
    status = response_json["response"]["request"]["status"]
    print("REQUEST STATUS: ", status)
    time.sleep(1)
    if checks == 15:
        raise Exception("Number of status checks exceeds limit. Possible problem with Path Trace.!")
    elif status == "FAILED":
        raise Exception("Problem with Path Trace - FAILED!")
    checks += 1


path_source = response_json["response"]["request"]["sourceIP"]
path_dest = response_json["response"]["request"]["destIP"]
networkElementsInfo = response_json["response"]["networkElementsInfo"]

all_devices = []
device_no = 1
for networkElement in networkElementsInfo:
    if "name" not in networkElement:
        name = "Unnamed Host"
        ip = networkElement["ip"]
        egressInterfaceName = "UNKNOWN"
        ingressInterfaceName = "UNKNOWN"
    else:
        name = networkElement["name"]
        ip = networkElement["ip"]
        if "egressInterface" in networkElement:
            egressInterfaceName = networkElement["egressInterface"]["physicalInterface"]["name"]
        else:
            egressInterfaceName = "UNKNOWN"

        if "ingressInterface" in networkElement:
            ingressInterfaceName = networkElement["ingressInterface"]["physicalInterface"]["name"]
        else:
            ingressInterfaceName = "UNKNOWN"
    
    device = [
                device_no,
                name,
                ip,
                ingressInterfaceName,
                egressInterfaceName
             ]
    all_devices.append(device)
    device_no += 1


print("Path trace: \n Source: ", path_source, "\n Destination: ", path_dest)  
print("List of devices on path:")
table_header = [
                "Item",
                "Name",
                "IP",
                "Ingress Int",
                "Egress Int"
               ]
print( tabulate(all_devices, table_header) )  
