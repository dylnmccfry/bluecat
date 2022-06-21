## update_dhcp_reservation.py
This script is used to create a DHCP reservation using an IP address, FQDN, and MAC address. Create a .csv file named **ips.csv**

The format is <IP>,<MAC>,<FQDN>

For example:

`10.10.10.10,AA-BB-CC-DD-EE-FF,my-hostname.domain.com`

`10.10.10.11,AA-BB-CC-DD-EE-F1,my-hostname2.domain.com`

## assign_ipv4_static.py
This script is used to create a static IPAM entry with a hostname. Create a .csv file named **statc_hosts.csv**

The format is <IP>,<Hostname>

For example:

`10.10.10.11,my-hostname1`

`10.10.10.12,my-hostname2`
