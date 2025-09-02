#!/usr/bin/python
"""
Custom Mininet Script for a 3-Router Network

This script creates a network topology with two hosts (h1, h2) and
three routers (r1, r2, r3). The routers are Mininet hosts configured
to forward IP packets.

Topology:
h1 -- r1 -- r2 -- r3 -- h2

IP Configuration:
- h1: 10.0.1.100/24, default gateway: 10.0.1.1 (r1)
- r1: 10.0.1.1/24 (to h1), 10.0.2.1/24 (to r2)
- r2: 10.0.2.2/24 (to r1), 10.0.3.1/24 (to r3)
- r3: 10.0.3.2/24 (to r2), 10.0.4.1/24 (to h2)
- h2: 10.0.4.100/24, default gateway: 10.0.4.1 (r3)

The script configures all IP addresses, static routes, and enables
IP forwarding on the routers.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, OVSController
from mininet.cli import CLI
from mininet.log import setLogLevel, info

class RouterTopo(Topo):
    """
    A topology with 2 hosts and 3 routers.
    h1 -- r1 -- r2 -- r3 -- h2
    """

    def build(self):
        "Create the custom topology."
        info('*** Adding Hosts\n')
        h1 = self.addHost('h1', ip='10.0.1.100/24', defaultRoute='via 10.0.1.1')
        h2 = self.addHost('h2', ip='10.0.4.100/24', defaultRoute='via 10.0.4.1')

        info('*** Adding Routers\n')
        # We add routers as hosts and will enable IP forwarding on them
        r1 = self.addHost('r1')
        r2 = self.addHost('r2')
        r3 = self.addHost('r3')

        info('*** Creating Links\n')
        # Links between hosts and routers
        self.addLink(h1, r1) # h1-eth0 <-> r1-eth0
        self.addLink(r1, r2) # r1-eth1 <-> r2-eth0
        self.addLink(r2, r3) # r2-eth1 <-> r3-eth0
        self.addLink(r3, h2) # r3-eth1 <-> h2-eth0


def configure_and_run():
    """
    Creates the network, configures routers, and runs the CLI.
    """
    topo = RouterTopo()

    # The controller is not strictly necessary for this static routing setup,
    # but is included as requested by the exercise prompt.
    net = Mininet(topo=topo, controller=OVSController)

    info('*** Starting network\n')
    net.start()

    # --- Router and Host Configuration ---
    info('*** Configuring routing and IP addresses\n')

    # Get node objects
    h1, h2 = net.get('h1', 'h2')
    r1, r2, r3 = net.get('r1', 'r2', 'r3')

    # Configure Router 1
    r1.cmd('ifconfig r1-eth0 10.0.1.1/24')
    r1.cmd('ifconfig r1-eth1 10.0.2.1/24')
    r1.cmd('sysctl net.ipv4.ip_forward=1')
    # Route to networks beyond r2
    r1.cmd('route add -net 10.0.3.0/24 gw 10.0.2.2')
    r1.cmd('route add -net 10.0.4.0/24 gw 10.0.2.2')

    # Configure Router 2
    r2.cmd('ifconfig r2-eth0 10.0.2.2/24')
    r2.cmd('ifconfig r2-eth1 10.0.3.1/24')
    r2.cmd('sysctl net.ipv4.ip_forward=1')
    # Route to h1's network
    r2.cmd('route add -net 10.0.1.0/24 gw 10.0.2.1')
    # Route to h2's network
    r2.cmd('route add -net 10.0.4.0/24 gw 10.0.3.2')

    # Configure Router 3
    r3.cmd('ifconfig r3-eth0 10.0.3.2/24')
    r3.cmd('ifconfig r3-eth1 10.0.4.1/24')
    r3.cmd('sysctl net.ipv4.ip_forward=1')
    # Route to networks beyond r2
    r3.cmd('route add -net 10.0.1.0/24 gw 10.0.3.1')
    r3.cmd('route add -net 10.0.2.0/24 gw 10.0.3.1')

    info('\n*** Routing Tables:\n')
    info('--- r1 ---\n')
    info(r1.cmd('route -n'))
    info('--- r2 ---\n')
    info(r2.cmd('route -n'))
    info('--- r3 ---\n')
    info(r3.cmd('route -n'))


    info('*** Testing network connectivity\n')
    # Ping from h1 to h2 to see if the routing works
    result = h1.cmd('ping -c 3 %s' % h2.IP())
    info(result + '\n')

    info('*** Running CLI\n')
    # Start the Mininet CLI for further interaction
    CLI(net)

    info('*** Stopping network\n')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    configure_and_run()
