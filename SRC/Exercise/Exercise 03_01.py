#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.log import setLogLevel, info

class MultiPathTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        # UDP routers
        r1, r2, r3 = [self.addHost(n) for n in ('r1', 'r2', 'r3')]
        # TCP routers
        r4, r5, r6 = [self.addHost(n) for n in ('r4', 'r5', 'r6')]
        # OTHER routers
        r7, r8, r9 = [self.addHost(n) for n in ('r7', 'r8', 'r9')]

        # Links UDP path
        self.addLink(h1, r1); self.addLink(r1, r2); self.addLink(r2, r3); self.addLink(r3, h2)
        # Links TCP path
        self.addLink(h1, r4); self.addLink(r4, r5); self.addLink(r5, r6); self.addLink(r6, h2)
        # Links OTHER path
        self.addLink(h1, r7); self.addLink(r7, r8); self.addLink(r8, r9); self.addLink(r9, h2)


def configure_and_run():
    topo = MultiPathTopo()
    net = Mininet(topo=topo, controller=OVSController)
    net.start()

    h1, h2 = net.get('h1', 'h2')
    r1, r2, r3 = net.get('r1', 'r2', 'r3')
    r4, r5, r6 = net.get('r4', 'r5', 'r6')
    r7, r8, r9 = net.get('r7', 'r8', 'r9')

    # --- Configure IPs ---
    # UDP path
    r1.setIP('10.0.1.1/24', intf='r1-eth0'); r1.setIP('10.0.2.1/24', intf='r1-eth1')
    r2.setIP('10.0.2.2/24', intf='r2-eth0'); r2.setIP('10.0.3.1/24', intf='r2-eth1')
    r3.setIP('10.0.3.2/24', intf='r3-eth0'); r3.setIP('10.0.4.1/24', intf='r3-eth1')
    h1.setIP('10.0.1.100/24', intf='h1-eth0'); h2.setIP('10.0.4.2/24', intf='h2-eth0')

    # TCP path
    r4.setIP('10.0.5.1/24', intf='r4-eth0'); r4.setIP('10.0.6.1/24', intf='r4-eth1')
    r5.setIP('10.0.6.2/24', intf='r5-eth0'); r5.setIP('10.0.7.1/24', intf='r5-eth1')
    r6.setIP('10.0.7.2/24', intf='r6-eth0'); r6.setIP('10.0.8.1/24', intf='r6-eth1')
    h1.setIP('10.0.5.100/24', intf='h1-eth1'); h2.setIP('10.0.8.2/24', intf='h2-eth1')

    # OTHER path
    r7.setIP('10.0.9.1/24', intf='r7-eth0'); r7.setIP('10.0.10.1/24', intf='r7-eth1')
    r8.setIP('10.0.10.2/24', intf='r8-eth0'); r8.setIP('10.0.11.1/24', intf='r8-eth1')
    r9.setIP('10.0.11.2/24', intf='r9-eth0'); r9.setIP('10.0.12.1/24', intf='r9-eth1')
    h1.setIP('10.0.9.100/24', intf='h1-eth2'); h2.setIP('10.0.12.2/24', intf='h2-eth2')

    # Enable forwarding
    for r in [r1, r2, r3, r4, r5, r6, r7, r8, r9]:
        r.cmd('sysctl -w net.ipv4.ip_forward=1')

    # --- Configure h1 policy routing ---
    h1.cmd('ip rule add fwmark 1 table 1')
    h1.cmd('ip rule add fwmark 2 table 2')
    h1.cmd('ip rule add fwmark 3 table 3')

    h1.cmd('ip route add default via 10.0.1.1 dev h1-eth0 table 1')
    h1.cmd('ip route add default via 10.0.5.1 dev h1-eth1 table 2')
    h1.cmd('ip route add default via 10.0.9.1 dev h1-eth2 table 3')

    # Mark packets by protocol
    h1.cmd('iptables -t mangle -A OUTPUT -p udp -j MARK --set-mark 1')
    h1.cmd('iptables -t mangle -A OUTPUT -p tcp -j MARK --set-mark 2')
    h1.cmd('iptables -t mangle -A OUTPUT ! -p tcp ! -p udp -j MARK --set-mark 3')

    # --- Configure h2 return routing ---
    # Create rules like h1 but reversed
    h2.cmd('ip rule add from 10.0.4.2 table 1')
    h2.cmd('ip rule add from 10.0.8.2 table 2')
    h2.cmd('ip rule add from 10.0.12.2 table 3')

    h2.cmd('ip route add default via 10.0.3.2 dev h2-eth0 table 1')
    h2.cmd('ip route add default via 10.0.7.2 dev h2-eth1 table 2')
    h2.cmd('ip route add default via 10.0.11.2 dev h2-eth2 table 3')

    info('*** Testing connectivity\n')
    info(h1.cmd('ping -c 2 10.0.4.2'))   # UDP path
    info(h1.cmd('ping -c 2 10.0.8.2'))   # TCP path
    info(h1.cmd('ping -c 2 10.0.12.2'))  # OTHER path

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    configure_and_run()
