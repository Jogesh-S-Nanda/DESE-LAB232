# Mininet CLI Commands

This document provides an overview of common Mininet CLI commands for creating, managing, and interacting with network topologies in Mininet.

## Starting Mininet
- **`mininet`**: Launch the Mininet CLI with a default topology (e.g., minimal topology with 2 hosts and 1 switch).
  ```
  sudo mn
  ```
- **`mn --topo=<topology>`**: Start Mininet with a specific topology (e.g., `linear`, `tree`, `single`, `torus`).
  ```
  sudo mn --topo=linear,4
  ```
  Example: Creates a linear topology with 4 switches and 4 hosts.

- **`mn --custom <file>.py --topo <toponame>`**: Use a custom topology defined in a Python script.
  ```
  sudo mn --custom custom_topo.py --topo mytopo
  ```

- **`mn --controller=<controller>`**: Specify the controller (e.g., `remote`, `ovsc`, `ref`).
  ```
  sudo mn --controller=remote,ip=127.0.0.1,port=6653
  ```

- **`mn --switch=<switch>`**: Specify the switch type (e.g., `ovsk`, `user`).
  ```
  sudo mn --switch=ovsk
  ```

## CLI Commands
Once in the Mininet CLI (`mininet>` prompt), you can use the following commands:

### General Commands
- **`help`**: Display available CLI commands.
  ```
  mininet> help
  ```

- **`nodes`**: List all nodes (hosts, switches, controllers) in the topology.
  ```
  mininet> nodes
  ```

- **`net`**: Display the network topology, showing connections between nodes.
  ```
  mininet> net
  ```

- **`dump`**: Dump information about all nodes, including IP addresses and PIDs.
  ```
  mininet> dump
  ```

- **`exit` or `quit`**: Exit the Mininet CLI and clean up the network.
  ```
  mininet> exit
  ```

### Host Commands
- **`<host> <command>`**: Run a command on a specific host (e.g., `h1`, `h2`).
  ```
  mininet> h1 ifconfig
  ```
  Example: Displays network interfaces for host `h1`.

- **`<host> ping <host>`**: Ping between two hosts to test connectivity.
  ```
  mininet> h1 ping h2
  ```

- **`pingall`**: Test connectivity between all pairs of hosts.
  ```
  mininet> pingall
  ```

- **`pingpair`**: Test connectivity between the first two hosts.
  ```
  mininet> pingpair
  ```

### Switch Commands
- **`dpctl <command>`**: Interact with OpenFlow switches (e.g., show flow tables).
  ```
  mininet> dpctl dump-flows
  ```

- **`ovs-vsctl <command>`**: Run Open vSwitch commands to manage switches.
  ```
  mininet> ovs-vsctl show
  ```
  Example: Displays the Open vSwitch configuration.

### Link and Interface Commands
- **`link <node1> <node2> up/down`**: Enable or disable a link between two nodes.
  ```
  mininet> link s1 h1 down
  ```

- **`intfs`**: List all interfaces in the network.
  ```
  mininet> intfs
  ```

### Testing and Performance
- **`iperf`**: Run iperf between two hosts to measure bandwidth.
  ```
  mininet> iperf h1 h2
  ```

- **`iperfudp`**: Run iperf in UDP mode to measure bandwidth and jitter.
  ```
  mininet> iperfudp h1 h2
  ```

### Python Interaction
- **`py <expression>`**: Execute a Python expression in the Mininet environment.
  ```
  mininet> py h1.IP()
  ```
  Example: Prints the IP address of host `h1`.

- **`sh <command>`**: Run a shell command from the Mininet CLI.
  ```
  mininet> sh ls
  ```

### Debugging and Monitoring
- **`xterm <node>`**: Open an xterm window for a specific node.
  ```
  mininet> xterm h1
  ```

- **`wireshark`**: Start Wireshark to capture packets (requires Wireshark installed).
  ```
  mininet> wireshark
  ```

### Custom Scripts
- **`source <script>.mn`**: Run a Mininet script file containing CLI commands.
  ```
  mininet> source myscript.mn
  ```

## Example Workflow
1. Start Mininet with a linear topology of 3 switches:
   ```
   sudo mn --topo=linear,3
   ```
2. Check the network topology:
   ```
   mininet> net
   ```
3. Test connectivity between all hosts:
   ```
   mininet> pingall
   ```
4. Open a terminal for host `h1`:
   ```
   mininet> xterm h1
   ```
5. Exit Mininet:
   ```
   mininet> exit
   ```

## Notes
- Most commands require `sudo` when starting Mininet due to network configuration privileges.
- Use `mn -c` to clean up Mininet processes if it exits abnormally:
  ```
  sudo mn -c
  ```

For more details, refer to the [Mininet documentation](http://mininet.org/walkthrough/#part-2-mininet-command-line-interface-cli).