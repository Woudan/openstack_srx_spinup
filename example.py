"""
 _______             ___________
 |      |           | ubuntu    |
 | SRX  |<--------->|(openstack)|
 |______|           |___________|
SRX has a trust and vpn zone, change script if other zones are used

* Netconf has to be enable on the SRX.
* Your active policy's between your trust and vpn policy will be used.
* At the moment configured with proposal sets that are allready configured in the SRX.

^^ This is just a for fun home project to easy deploy testing services. Would not be usefull
anymore when the neutron vpn service is implementated in all openstack setups. @the moment OVH
does not support this yet.
"""

from JuniperSrx import JuniperSrx
from Openstack import Openstack

# instance information
instance_name = "testinstance-3"
remoteipprivate = "ip"

# openstack post-creation script
instance_username = "admin"
instance_password_hash = "password hash"

# SRX data
srx_ip = "192.168.1.1"
srx_username = "root"
srx_password = "password"
srx_free_st = "st0.3"
srx_public_ip = "ip"

# Openstack credentials
openstack_auth_url="https://auth.cloud.ovh.net/v2.0/"
openstack_username="username"
openstack_password="password"
openstack_tenant_name="tennant-id"

# Create openstack instance
openstack = Openstack()
create_instance = openstack.create_server(hostname=instance_name,
                                          auth_url=openstack_auth_url,
                                          username=openstack_username,
                                          password=openstack_password,
                                          tenant_name=openstack_tenant_name,
                                          remoteipprivate=remoteipprivate + "/32",
                                          instance_username=instance_username,
                                          instance_password=instance_password_hash)

# create juniper SRX configuration
commit_srx = JuniperSrx(hostname=instance_name,
                        remoteippublic=create_instance[1],
                        remoteipprivate=remoteipprivate,
                        tunnelint=srx_free_st,
                        username=srx_username,
                        password=srx_password,
                        srxip=srx_ip)

print create_instance[0]
print create_instance[1]
print commit_srx.commitConfiguration()
