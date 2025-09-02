from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def create_network():
    # Set log level to info for output
    setLogLevel('info')

    # Create a Mininet object
    net = Mininet(controller=Controller, switch=OVSSwitch)

    # Add controller
    #info("*** Adding controller\n")
    #c0 = net.addController('c0')

    # Add switches
    info("*** Adding switches\n")
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')

    # Add hosts
    info("*** Adding hosts\n")
    h1 = net.addHost('h1', ip='10.0.0.10/24')
    h2 = net.addHost('h2', ip='10.0.0.20/24')

    # Add links
    info("*** Creating links\n")
    net.addLink(h1, s1)
    net.addLink(s1, s2)
    net.addLink(s2, h2)

    # Start the network
    info("*** Starting network\n")
    net.start()

    # Open Mininet CLI
    info("*** Running CLI\n")
    CLI(net)

    # Stop the network
    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    create_network()