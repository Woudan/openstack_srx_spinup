# Openstack + SRX auto vpn

Scripting to automatically create a vpn with Racoon and Juniper to an Openstack environment.
- Creates an openstack instance
- Setups up Racoon with vpn configuration ( With some other stuff, admin account etc.)
- Creates a Juniper SRX vpn configuration

Issues:
- Openstack loopback interface is not recognized correctly so it hangs for 120 seconds
- Route is with private source address is not automatically added yet
- Racoon sometimes hangs with startup so a manual restart has to be given.
- Clean up the code
- No error checking yet

----------------------------------------------------------------
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