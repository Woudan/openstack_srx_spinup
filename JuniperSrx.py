from jnpr.junos import Device
from jnpr.junos.utils.config import Config


class JuniperSrx(object):

    def __init__(self, srxip=None, username=None, password=None, hostname=None, remoteippublic=None,
                 remoteipprivate=None, tunnelint=None):
        self.srxip = srxip
        self.username = username
        self.password = password
        self.hostname = hostname
        self.remoteippublic = remoteippublic
        self.remoteipprivate = remoteipprivate
        self.tunnelint = tunnelint

    def checkConnection(self):
        return "It's working"

    def commitConfiguration(self):
        dev = Device(host=self.srxip, user=self.username, password=self.password)
        dev.open()
        cu = Config(dev)
        config = """ set routing-options static route %s/32 next-hop %s
set interfaces %s family inet
set security zones security-zone vpn interfaces %s
set security ike gateway gateway-%s ike-policy pol-basic
set security ike gateway gateway-%s address %s
set security ike gateway gateway-%s external-interface ge-0/0/0.0
set security ipsec vpn vpn-%s bind-interface %s
set security ipsec vpn vpn-%s ike gateway gateway-%s
set security ipsec vpn vpn-%s ike proxy-identity local 192.168.1.0/26
set security ipsec vpn vpn-%s ike proxy-identity remote %s/32
set security ipsec vpn vpn-%s ike ipsec-policy pol-basic
set security ipsec vpn vpn-%s establish-tunnels immediately
        """ % (self.remoteipprivate, self.tunnelint, self.tunnelint, self.tunnelint, self.hostname,
               self.hostname, self.remoteippublic, self.hostname, self.hostname, self.tunnelint, self.hostname,
               self.hostname, self.hostname, self.hostname, self.remoteipprivate, self.hostname, self.hostname)
        cu.load(config, format="set")
        cu.commit()
        dev.close()
        return "committed config: \n" + config




