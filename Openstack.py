from keystoneclient.auth.identity import v2
from keystoneclient import session
from novaclient import client
from glanceclient import Client
import time


class Openstack(object):

    def create_server(self, hostname, auth_url, username, password, tenant_name, remoteipprivate,
                      instance_username, instance_password):
        """ Creates a server with post creation configuration within you openstack environment.
        :param hostname:
        :return instance_id, instance_ip:
        """

        # Create all
        auth = v2.Password(auth_url=auth_url,
                           username=username,
                           password=password,
                           tenant_name=tenant_name)

        sess = session.Session(auth=auth)
        nova = client.Client(2, session=sess)

        fl = nova.flavors.find(name="vps-ssd-1")

        glance = Client('2', session=sess)
        #print nova.flavors.list()
        # #print fl

        # Post init data | change with own configuration | Must change pub
        userdata = """#!/bin/bash
        echo 'Bash script for racoon setup and user'
        useradd -m %s
        usermod --password '%s' %s
        echo '%s    ALL=(ALL:ALL) ALL' >> /etc/sudoers
        apt-get upgrade
        apt-get install racoon -y
        echo '# loopback interface for ipsec vpn
auto lo:10
iface lo:10 inet static
    address %s
    netmask 255.255.255.255' >> /etc/network/interfaces
        echo -e '# IPv4/v6 addresses\n84.26.174.191   51hZrqA$' >> /etc/racoon/psk.txt
        ip=`/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'`
        echo $ip
        echo -e '#
# NOTE: This file will not be used if you use racoon-tool(8) to manage your
# IPsec connections. racoon-tool will process racoon-tool.conf(5) and
# generate a configuration (/var/lib/racoon/racoon.conf) and use it, instead
# of this file.
#
# Simple racoon.conf
#
#
# Please look in /usr/share/doc/racoon/examples for
# examples that come with the source.
#
# Please read racoon.conf(5) for details, and alsoread setkey(8).
#
#
# Also read the Linux IPSEC Howto up at
# http://www.ipsec-howto.org/t1.html
#
path pre_shared_key "/etc/racoon/psk.txt";

remote 84.26.174.191 {
        exchange_mode main;
        proposal {
                encryption_algorithm 3des;
                hash_algorithm md5;
                authentication_method pre_shared_key;
                dh_group modp1024;
        }
}
sainfo address %s any address 192.168.1.0/26 any {
        lifetime time 1 hour;
        encryption_algorithm 3des;
        authentication_algorithm hmac_md5;
        compression_algorithm deflate;

}' > /etc/racoon/racoon.conf

        echo -e "#!/usr/sbin/setkey -f
## Flush the SAD and SPD
#
flush;
spdflush;
## Security policy definitions for our test subnets
spdadd %s 192.168.1.0/26 any -P out ipsec
           esp/tunnel/$ip-84.26.174.191/require;

spdadd 192.168.1.0/26 %s any -P in ipsec
           esp/tunnel/84.26.174.191-$ip/require;
        " > /etc/ipsec-tools.conf
service setkey restart
chmod 600 /etc/racoon/psk.txt
reboot
        """ % (instance_username, instance_password, instance_username, instance_username,
               remoteipprivate, remoteipprivate, remoteipprivate, remoteipprivate)

        # create instance
        create_instance = nova.servers.create(hostname, flavor=fl, image="9bfac38c-688f-4b63-bf3b-69155463c0e7", userdata=userdata)

        # Wait to retrieve data
        time.sleep(10)

        # Output possible usefull data | could be returned for SRX script
        return create_instance.id, nova.servers.ips(create_instance.id)['Ext-Net'][0]['addr']