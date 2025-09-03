#!/usr/bin/python
"""
Mininet Exercise - Lab 03 - Question 1

This script creates a network topology based on the provided diagram
and implements policy-based routing to direct traffic based on its protocol.

Topology:
 h1 -- s1 -- r1 -- r2 -- r3 -- s2 -- h2
         |-- r4 -- r5 -- r6 --|
         |-- r7 -- r8 -- r9 --|

Routing Rules:
- UDP packets from h1 to h2 travel via the r1-r2-r3 path.
- TCP packets from h1 to h2 travel via the r4-r5-r6 path.
- All other traffic (ICMP, ARP, etc.) travels via the r7-r8-r9 path.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter(Node):
    """A Node with IP forwarding enabled to act as a router."""

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl -w net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl -w net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    """
    Creates the custom network topology.
    All "routers" are initially created as standard hosts.
    The LinuxRouter class or manual configuration will be used to enable forwarding.
    """

    def build(self, **_opts):
        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        # Add routers using our custom LinuxRouter class
        routers = {i: self.addNode(f'r{i}', cls=LinuxRouter) for i in range(1, 10)}

        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # --- Connect the network elements ---

        # Connect host h1 to the entry switch s1
        self.addLink(h1, s1)

        # Connect entry switch s1 to the start of each router path
        self.addLink(s1, routers[1])  # s1 -> r1
        self.addLink(s1, routers[4])  # s1 -> r4
        self.addLink(s1, routers[7])  # s1 -> r7

        # Connect the routers in their respective paths
        # Path 1 (for UDP)
        self.addLink(routers[1], routers[2])  # r1 -> r2
        self.addLink(routers[2], routers[3])  # r2 -> r3

        # Path 2 (for TCP)
        self.addLink(routers[4], routers[5])  # r4 -> r5
        self.addLink(routers[5], routers[6])  # r5 -> r6

        # Path 3 (for other traffic)
        self.addLink(routers[7], routers[8])  # r7 -> r8
        self.addLink(routers[8], routers[9])  # r8 -> r9

        # Connect the end of each router path to the exit switch s2
        self.addLink(routers[3], s2)  # r3 -> s2
        self.addLink(routers[6], s2)  # r6 -> s2
        self.addLink(routers[9], s2)  # r9 -> s2

        # Connect exit switch s2 to host h2
        self.addLink(s2, h2)


def run_network():
    """
    Initializes and configures the Mininet network.
    """
    # Clean up any previous Mininet runs
    # mn -c > /dev/null 2>&1

    topo = NetworkTopo()
    net = Mininet(topo=topo, controller=None)  # No controller needed for L3 routing
    net.start()

    # --- Node Configuration ---
    info('*** Configuring network nodes...\n')

    # Get node objects from the network
    h1, h2 = net.get('h1', 'h2')
    r = {i: net.get(f'r{i}') for i in range(1, 10)}

    # --- IP Address Configuration ---
    # Note: Mininet automatically assigns interface names like 'r1-eth0', 'r1-eth1', etc.
    # The order depends on the order links were created in the build() method.

    # Configure h1
    h1.setIP('192.168.1.1', 24, intf='h1-eth0')

    # Configure h2
    h2.setIP('192.168.2.1', 24, intf='h2-eth0')

    # Configure router interfaces connected to s1 (entry point)
    r[1].setIP('192.168.1.101', 24, intf='r1-eth0')
    r[4].setIP('192.168.1.104', 24, intf='r4-eth0')
    r[7].setIP('192.168.1.107', 24, intf='r7-eth0')

    # Configure router interfaces connected to s2 (exit point)
    r[3].setIP('192.168.2.103', 24, intf='r3-eth1')
    r[6].setIP('192.168.2.106', 24, intf='r6-eth1')
    r[9].setIP('192.168.2.109', 24, intf='r9-eth1')

    # Configure inter-router links
    # Path 1 (r1-r2-r3)
    r[1].setIP('10.0.1.1', 24, intf='r1-eth1')
    r[2].setIP('10.0.1.2', 24, intf='r2-eth0')
    r[2].setIP('10.0.2.1', 24, intf='r2-eth1')
    r[3].setIP('10.0.2.2', 24, intf='r3-eth0')

    # Path 2 (r4-r5-r6)
    r[4].setIP('10.0.3.1', 24, intf='r4-eth1')
    r[5].setIP('10.0.3.2', 24, intf='r5-eth0')
    r[5].setIP('10.0.4.1', 24, intf='r5-eth1')
    r[6].setIP('10.0.4.2', 24, intf='r6-eth0')

    # Path 3 (r7-r8-r9)
    r[7].setIP('10.0.5.1', 24, intf='r7-eth1')
    r[8].setIP('10.0.5.2', 24, intf='r8-eth0')
    r[8].setIP('10.0.6.1', 24, intf='r8-eth1')
    r[9].setIP('10.0.6.2', 24, intf='r9-eth0')

    # --- Static Routing on Routers ---
    info('*** Configuring static routes on routers...\n')
    # Path 1
    r[1].cmd('ip route add 192.168.2.0/24 via 10.0.1.2')
    r[2].cmd('ip route add 192.168.1.0/24 via 10.0.1.1')
    r[2].cmd('ip route add 192.168.2.0/24 via 10.0.2.2')
    r[3].cmd('ip route add 192.168.1.0/24 via 10.0.2.1')
    # Path 2
    r[4].cmd('ip route add 192.168.2.0/24 via 10.0.3.2')
    r[5].cmd('ip route add 192.168.1.0/24 via 10.0.3.1')
    r[5].cmd('ip route add 192.168.2.0/24 via 10.0.4.2')
    r[6].cmd('ip route add 192.168.1.0/24 via 10.0.4.1')
    # Path 3
    r[7].cmd('ip route add 192.168.2.0/24 via 10.0.5.2')
    r[8].cmd('ip route add 192.168.1.0/24 via 10.0.5.1')
    r[8].cmd('ip route add 192.168.2.0/24 via 10.0.6.2')
    r[9].cmd('ip route add 192.168.1.0/24 via 10.0.6.1')

    # --- Policy-Based Routing on h1 ---
    info('*** Configuring policy-based routing on h1...\n')
    # 1. Create new routing tables in /etc/iproute2/rt_tables
    h1.cmd('echo "10 udp_table" >> /etc/iproute2/rt_tables')
    h1.cmd('echo "20 tcp_table" >> /etc/iproute2/rt_tables')

    # 2. Define routes for each table
    h1.cmd('ip route add 192.168.2.0/24 via 192.168.1.101 table udp_table')
    h1.cmd('ip route add 192.168.2.0/24 via 192.168.1.104 table tcp_table')

    # 3. Mark packets with iptables
    h1.cmd('iptables -A OUTPUT -t mangle -p udp -j MARK --set-mark 1')
    h1.cmd('iptables -A OUTPUT -t mangle -p tcp -j MARK --set-mark 2')

    # 4. Add rules to use the new tables for marked packets
    h1.cmd('ip rule add fwmark 1 lookup udp_table')
    h1.cmd('ip rule add fwmark 2 lookup tcp_table')

    # 5. Add a default route for all other traffic
    h1.cmd('ip route add default via 192.168.1.107')

    # --- Configure h2's Default Route ---
    # This allows h2 to reply to h1
    info('*** Configuring default route on h2...\n')
    h2.cmd('ip route add default via 192.168.2.109')

    # --- Verification Instructions ---
    info("\n*** Configuration Complete. The network is ready. ***\n")
    info("***\n")
    info("*** HOW TO TEST THE ROUTES:\n")
    info("1. Open terminals for routers r1, r4, r7 using the Mininet CLI:\n")
    info("   mininet> xterm r1 r4 r7\n")
    info("2. In each new terminal, start tcpdump to monitor traffic:\n")
    info("   - In r1's terminal: tcpdump -n -i r1-eth1\n")
    info("   - In r4's terminal: tcpdump -n -i r4-eth1\n")
    info("   - In r7's terminal: tcpdump -n -i r7-eth1\n")
    info("3. Open a terminal for h2 and start an iperf server:\n")
    info("   mininet> xterm h2\n")
    info("   - In h2's terminal: iperf -s\n")
    info("4. From the main Mininet CLI, run these commands on h1:\n")
    info("   - Test ICMP (default route r7-r8-r9):\n")
    info("     mininet> h1 traceroute 192.168.2.1\n")
    info("   - Test UDP (route r1-r2-r3):\n")
    info("     mininet> h1 iperf -c 192.168.2.1 -u -b 1M\n")
    info("     (You should see UDP traffic in r1's tcpdump window)\n")
    info("   - Test TCP (route r4-r5-r6):\n")
    info("     mininet> h1 iperf -c 192.168.2.1 -t 10\n")
    info("     (You should see TCP traffic in r4's tcpdump window)\n")
    info("***\n")

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run_network()
