from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch, Host
from mininet.cli import CLI
from mininet.log import setLogLevel
import time

def setup_network():
    # Create Mininet object
    net = Mininet(controller=Controller, switch=OVSSwitch)

    # Add controller
    #c0 = net.addController('c0')

    # Add hosts
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.1.2/24')

    # Add routers (using switches with IP forwarding)
    r1 = net.addSwitch('r1')
    r2 = net.addSwitch('r2')
    r3 = net.addSwitch('r3')
    r4 = net.addSwitch('r4')
    r5 = net.addSwitch('r5')
    r6 = net.addSwitch('r6')
    r7 = net.addSwitch('r7')
    r8 = net.addSwitch('r8')
    r9 = net.addSwitch('r9')

    # Create links
    # Path 1: h1 -> r1 -> r2 -> r3 -> h2
    net.addLink(h1, r1)
    net.addLink(r1, r2)
    net.addLink(r2, r3)
    net.addLink(r3, h2)

    # Path 2: h1 -> r4 -> r5 -> r6 -> h2
    net.addLink(h1, r4)
    net.addLink(r4, r5)
    net.addLink(r5, r6)
    net.addLink(r6, h2)

    # Path 3: h1 -> r7 -> r8 -> r9 -> h2
    net.addLink(h1, r7)
    net.addLink(r7, r8)
    net.addLink(r8, r9)
    net.addLink(r9, h2)

    # Start the network
    net.start()

    # Assign IP addresses to router interfaces
    # Path 1
    r1.cmd('ifconfig r1-eth0 10.1.1.1/24')
    r1.cmd('ifconfig r1-eth1 10.1.2.1/24')
    r2.cmd('ifconfig r2-eth0 10.1.2.2/24')
    r2.cmd('ifconfig r2-eth1 10.1.3.1/24')
    r3.cmd('ifconfig r3-eth0 10.1.3.2/24')
    r3.cmd('ifconfig r3-eth1 10.1.4.1/24')

    # Path 2
    r4.cmd('ifconfig r4-eth0 10.2.1.1/24')
    r4.cmd('ifconfig r4-eth1 10.2.2.1/24')
    r5.cmd('ifconfig r5-eth0 10.2.2.2/24')
    r5.cmd('ifconfig r5-eth1 10.2.3.1/24')
    r6.cmd('ifconfig r6-eth0 10.2.3.2/24')
    r6.cmd('ifconfig r6-eth1 10.2.4.1/24')

    # Path 3
    r7.cmd('ifconfig r7-eth0 10.3.1.1/24')
    r7.cmd('ifconfig r7-eth1 10.3.2.1/24')
    r8.cmd('ifconfig r8-eth0 10.3.2.2/24')
    r8.cmd('ifconfig r8-eth1 10.3.3.1/24')
    r9.cmd('ifconfig r9-eth0 10.3.3.2/24')
    r9.cmd('ifconfig r9-eth1 10.3.4.1/24')

    # Enable IP forwarding on routers
    for router in [r1, r2, r3, r4, r5, r6, r7, r8, r9]:
        router.cmd('sysctl -w net.ipv4.ip_forward=1')

    # Configure routing tables on h1 for protocol-based routing
    # UDP via r1-r2-r3
    h1.cmd('ip rule add ipproto udp table 1')
    h1.cmd('ip route add 10.0.1.0/24 via 10.1.1.1 dev h1-eth0 table 1')

    # TCP via r4-r5-r6
    h1.cmd('ip rule add ipproto tcp table 2')
    h1.cmd('ip route add 10.0.1.0/24 via 10.2.1.1 dev h1-eth1 table 2')

    # Other traffic via r7-r8-r9
    h1.cmd('ip rule add table 3')
    h1.cmd('ip route add 10.0.1.0/24 via 10.3.1.1 dev h1-eth2 table 3')

    # Default route for h1 (optional, for unrouted traffic)
    h1.cmd('ip route add default via 10.3.1.1')

    # Configure routing tables on h2
    h2.cmd('ip route add 10.0.0.0/24 via 10.1.4.1')  # For UDP
    h2.cmd('ip route add 10.0.0.0/24 via 10.2.4.1')  # For TCP
    h2.cmd('ip route add 10.0.0.0/24 via 10.3.4.1')  # For other

    # Configure routing tables on routers
    # Path 1: r1 -> r2 -> r3
    r1.cmd('ip route add 10.0.1.0/24 via 10.1.2.2')
    r2.cmd('ip route add 10.0.1.0/24 via 10.1.3.2')
    r3.cmd('ip route add 10.0.0.0/24 via 10.1.2.1')

    # Path 2: r4 -> r5 -> r6
    r4.cmd('ip route add 10.0.1.0/24 via 10.2.2.2')
    r5.cmd('ip route add 10.0.1.0/24 via 10.2.3.2')
    r6.cmd('ip route add 10.0.0.0/24 via 10.2.2.1')

    # Path 3: r7 -> r8 -> r9
    r7.cmd('ip route add 10.0.1.0/24 via 10.3.2.2')
    r8.cmd('ip route add 10.0.1.0/24 via 10.3.3.2')
    r9.cmd('ip route add 10.0.0.0/24 via 10.3.2.1')

    # Start CLI for manual testing
    CLI(net)

    # Stop the network
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    setup_network()