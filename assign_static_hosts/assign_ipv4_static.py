import requests
import getpass
import json
import csv

username = 'username'
password = 'password'
bam_url = "yourbam.domain.com"
# Object ID of the parent container
config_id = 100001
# Predefined action found here https://docs.bluecatnetworks.com/r/Address-Manager-API-Guide/IP-assignment-action-values/9.3.0
action = "MAKE_STATIC"
# Container Object ID for the 10.0.0.0/8 network
container = 100002

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

device_ip_list = []
device_hostname_list = []
with open("static_hosts.csv", 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        device_ip_list.append(row[0])
        device_hostname_list.append(row[1])


# Checks each IP address to see if it has been assigned and if it has valid data
for ip_address, hostname in zip(device_ip_list, device_hostname_list):
    bam_get_ip_url = f"http://{bam_url}/Services/REST/v1/getIP4Address?address={ip_address}&containerId={container}"
    r = requests.get(bam_get_ip_url, headers=headers)
    print(r.text)
    ip_to_update = json.loads(r.text)
    object_id = int(ip_to_update.get('id'))
    if ip_to_update.get('id') == 0:
        print('This address is not currently assigned. Creating new object in Bluecat.')
# This is where the script would set the reservation

# POST URL to update DHCP reservation with MAC address and hostname
        bam_post_url = f"http://{bam_url}/Services/REST/v1/assignIP4Address?action={action}&configurationId={config_id}&ip4Address={ip_address}&properties=name={hostname}"
        r = requests.post(bam_post_url, headers=headers)
        print(r)
        print(r.text)

# Deletes object if it exists and then posts update
    else:
        print('This address already exists.')
# This is where the script would delete the existing object, and then create the reservation.
        print(object_id, 'is being deleted...')
        bam_delete_url = f"http://{bam_url}/Services/REST/v1/delete?objectId={object_id}"
        r = requests.delete(bam_delete_url, headers=headers)
        print(r)
        print(r.text)
        print('')
        print('Creating static IP assignment...')
        bam_post_url = f"http://{bam_url}/Services/REST/v1/assignIP4Address?action={action}&configurationId={config_id}&ip4Address={ip_address}&properties=name={hostname}"
        r = requests.post(bam_post_url, headers=headers)
        print(r)
        print(r.text)
