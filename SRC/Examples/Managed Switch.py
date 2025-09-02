#!/usr/bin/python
"""
Custom Topology Script for Mininet

This script creates a simple network topology with two hosts (h1, h2)
and two switches (s1, s2). The connections are as follows:

h1 <--> s1 <--> s2 <--> h2

This setup allows for testing connectivity and routing between two
separate network segments connected by a switch-to-switch link.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, OVSController
from mininet.cli import CLI
from mininet.log import setLogLevel, info


class ManagedSwitchTopo(Topo):
    """
    A simple custom topology of 2 hosts and 2 switches.
    h1 --- s1 --- s2 --- h2
    """

    def build(self):
        "Create the custom topology."
        info('*** Adding Hosts\n')
        # Add two hosts to the topology
        host1 = self.addHost('h1')
        host2 = self.addHost('h2')

        info('*** Adding Switches\n')
        # Add two switches to the topology
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')

        info('*** Creating Links\n')
        # Add links between the network components
        # Host 1 is connected to Switch 1
        self.addLink(host1, switch1)
        # Switch 1 is connected to Switch 2
        self.addLink(switch1, switch2)
        # Host 2 is connected to Switch 2
        self.addLink(host2, switch2)


def run_topology():
    """
    This function creates an instance of the topology,
    starts the Mininet network, runs a simple test,
    and opens the Mininet CLI for user interaction.
    """
    # Create an instance of our custom topology
    topo = ManagedSwitchTopo()

    # Create a Mininet network using the custom topology.
    # We specify controller=Controller to use Mininet's default
    # controller class. This requires a controller executable
    # (like ovs-controller) to be available in the system's PATH.
    net = Mininet(topo=topo, controller=OVSController)
    #net.addController('c0')

    info('*** Starting network\n')
    net.start()

    info('*** Testing network connectivity\n')
    # Use pingAll to check if all hosts can reach each other
    # The output will show the connectivity results and any packet loss.
    net.pingAll()

    info('*** Running CLI\n')
    # Start the Mininet command-line interface
    # You can run commands like 'h1 ping h2' or 'net'
    CLI(net)

    info('*** Stopping network\n')
    # Cleanly stop the network and remove virtual interfaces
    net.stop()


if __name__ == '__main__':
    # Set the logging level to 'info' to see status messages
    setLogLevel('info')
    # Execute the main function to run the topology
    run_topology()

