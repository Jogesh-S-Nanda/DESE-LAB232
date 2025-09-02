from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, Host
from mininet.cli import CLI
from mininet.log import setLogLevel

def create_network():
    # Create a Mininet object
    net = Mininet(controller=Controller, switch=OVSKernelSwitch)

    # Add controller
    c0 = net.addController('c0')

    # Add routers (using switches with IP forwarding)
    r1 = net.addSwitch('r1')
    r2 = net.addSwitch('r2')
    r3 = net.addSwitch('r3')

    # Add hosts
    h1 = net.addHost('h1', ip='10.0.1.2/24')
    h2 = net.addHost('h2', ip='10.0.2.2/24')

    # Add links
    net.addLink(h1, r1)
    net.addLink(r1, r2)
    net.addLink(r2, r3)
    net.addLink(r3, h2)

    # Start the network
    net.start()

    # Configure router interfaces
    r1.cmd('ifconfig r1-eth0 10.0.1.1/24')
    r1.cmd('ifconfig r1-eth1 10.0.3.1/24')
    r2.cmd('ifconfig r2-eth0 10.0.3.2/24')
    r2.cmd('ifconfig r2-eth1 10.0.4.1/24')
    r3.cmd('ifconfig r3-eth0 10.0.4.2/24')
    r3.cmd('ifconfig r3-eth1 10.0.2.1/24')

    # Enable IP forwarding on routers
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')

    # Add routing rules
    h1.cmd('ip route add default via 10.0.1.1')
    h2.cmd('ip route add default via 10.0.2.1')
    r1.cmd('ip route add 10.0.2.0/24 via 10.0.3.2')
    r2.cmd('ip route add 10.0.1.0/24 via 10.0.3.1')
    r2.cmd('ip route add 10.0.2.0/24 via 10.0.4.2')
    r3.cmd('ip route add 10.0.1.0/24 via 10.0.4.1')

    # Start CLI
    CLI(net)

    # Stop the network
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_network()