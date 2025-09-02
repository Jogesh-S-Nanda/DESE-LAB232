# TCPIP Networking Lab3: Mininet
# Description: Creating a custom network topology using a python program
# Topology: h1 ----- s1 ----- s2 ----- h2

# import necessary packages (we are importing subpackage Topo from the mininet package)
from mininet.topo import Topo

# create a class object
class lab2custom( Topo ):

	def __init__(self):
	
		Topo.__init__( self )
		
    # adding hosts
		h1 = self.addHost('h1', ip='10.0.0.1/24', netmask='255.255.255.0')
		h2 = self.addHost('h2', ip='10.0.0.2/24', netmask='255.255.255.0')

    # adding switches
		s1 = self.addSwitch('s1')
		s2 = self.addSwitch('s2')

    # adding links between hosts and switches
		self.addLink(h1,s1)
		self.addLink(h2,s2)
		self.addLink(s1,s2)

# naming the topology ('lab3switchtopology' is the topology name and lab3custom is the class name and filename)
topos = { 'lab3switchtopology': (lambda: lab2custom() )}
