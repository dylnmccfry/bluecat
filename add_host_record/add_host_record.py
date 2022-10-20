import requests
import getpass
import csv

username = input("Username:")
password = getpass.getpass()

#############################################
#########EDIT THESE VARIABLES################
#############################################
# FQDN of BAM or IP address of BAM
bam_url = "yourbam.domain.com"
# Object ID of the parent view
view_id = 123456
# TTL of host record in seconds
ttl = 86400

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

# Read csv file and create A records via POST method
with open('host_records.csv', 'r') as file:
    reader = csv.reader(file, delimiter = ',')
    for row in reader:
        fqdn = row[0]
        address = row[1]
        bam_add_host_record_url = f"http://{bam_url}/Services/REST/v1/addHostRecord?absoluteName={fqdn}&addresses={address}&ttl={ttl}&viewId={view_id}"
        r = requests.post(bam_add_host_record_url, headers=headers)
        if r.ok:
            print('Successfully created host record:', fqdn, 'Object ID:', r.text)
        else:
            print('Something went wrong, host record was not created successfully...')