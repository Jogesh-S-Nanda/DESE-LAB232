#!/usr/bin/python

"""
This script creates a custom network topology in Mininet.
The topology consists of:
- 1 Controller (c0)
- 2 Switches (s1, s2)
- 2 Hosts (h1, h2)

Host IPs are assigned as follows:
- h1: 10.0.0.10/24
- h2: 10.0.0.20/24

The network links are:
h1 <--> s1 <--> s2 <--> h2
"""

from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.clean import cleanup

cleanup()

def create_topology():
    "Create and run the custom network."

    # 1. Create a Mininet object
    # Run OVS switches in standalone mode; no external controller needed.
    net = Mininet(controller=None, switch=OVSSwitch, link=TCLink, autoSetMacs=True)

    info('*** Adding controller\n')
    # No local controller is added to avoid dependency on the missing 'controller' executable

    info('*** Adding hosts\n')
    # Add two hosts, h1 and h2
    # Assign the specified IP and netmask (CIDR notation /24 is 255.255.255.0)
    h1 = net.addHost('h1', ip='10.0.0.10/24')
    h2 = net.addHost('h2', ip='10.0.0.20/24')

    info('*** Adding switches\n')
    # Add two switches, s1 and s2, in standalone mode (no controller required)
    s1 = net.addSwitch('s1', failMode='standalone')
    s2 = net.addSwitch('s2', failMode='standalone')

    info('*** Creating links\n')
    # Create links between the nodes
    net.addLink(h1, s1)
    net.addLink(s1, s2)
    net.addLink(h2, s2)

    info('*** Starting network\n')
    # Start the network (switches will run standalone)
    net.start()

    info('*** Running CLI\n')
    # Start the Mininet Command Line Interface
    CLI(net)

    info('*** Stopping network\n')
    # Stop the network when the CLI is exited
    net.stop()

if __name__ == '__main__':
    # Set the logging level to 'info' to see the script's output
    setLogLevel('info')
    create_topology()
