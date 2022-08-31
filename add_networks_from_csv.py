import requests
import requests
import getpass
import json
import csv

username = 'username'
password = 'password'
bam_url = "yourbam.domain.com"
network = []
name = []
vlan = []
# Parent ID means Block that this network should be contained in
parent_id = 12345
type = "IP4Network"

# Login to Bluecat and generate token to be used for API calls
bam_login_url = f"http://{bam_url}/Services/REST/v1/login?username={username}&password={password}"
r = requests.get(bam_login_url)
bam_token = r.text
bam_token = bam_token.split(" ")
bam_token = (bam_token[2], bam_token[3])
bam_token = (" ".join(bam_token))

# Assign headers for API calls using token and json content type
headers = {
    "Content-Type": "application/json",
    "Authorization": bam_token
}
# Read csv file and create list of CIDR, name, vlan
with open('import_networks.csv', 'r') as file:
    reader = csv.reader(file, delimiter = ',')
    for row in reader:
        print(row)
        network.append(row[0])
        name.append(row[1])
        vlan.append(row[2])
# Using lists create networks within parent block
for cidr, net_name, vlan_id in zip(network, name, vlan):
    bam_add_network_url = f"http://{bam_url}/Services/REST/v1/addIP4Network?CIDR={cidr}&blockId={parent_id}&properties=udfVlanID={vlan_id}|name={net_name}"
    r = requests.post(bam_add_network_url, headers=headers)
# Print object ID of newly created object
    print(r.text)
