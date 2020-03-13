#!usr/bin/python

from mininet.topo import Topo

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController

REMOTE_CONTROLLER_IP = "192.168.1.70"

def simpleTest():
    topo = SingleLoopTopo()
    net = Mininet(topo=topo,
            controller=None,
            autoStaticArp=True)
    net.addController("c0",
            controller=RemoteController,
            ip=REMOTE_CONTROLLER_IP,
            port=6633)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectiviy"
    net.pingAll()
    net.stop()

class SingleLoopTopo(Topo):
    def __init__(self, **opts):
        Topo.__init__(self, **opts)
        n_s = int(input("Cuantos swiches utilizara?"))
        n_h = int(input("Cuantos hosts utilizara?"))
        switches = []
        hosts = []
        for s in range(n_s):
            switches.append(self.addSwitch('s%s' % (s + 1), protocols="OpenFlow13"))

        for h in range(n_h):
            hosts.append(self.addHost('h%s' % (h + 1)))

        opc = 0
        while opc != 3:
            opc = int(raw_input("Seleccione una opción:\n 1. Conectar Host con Switch\n 2. Conectar Switch con Switch\n 3. Ejecutar SDN"))
            if opc == 1:
                for h in range(n_h):
                    print((h + 1) + ", ")
                pos_h = int(input("Seleccione el host: "))

                for s in range(n_s):
                    print((s + 1) + ", ")
                pos_s = int(input("Seleccione el switch: "))

                self.addLink(hosts[pos_h - 1], switches[pos_s - 1])
            if opc == 2:
                for s in range(n_s):
                    print((s + 1) + ", ")
                pos_s1 = int(input("Seleccione el switch 1: "))

                for s in range(n_s):
                    print((s + 1) + ", ")
                pos_s2 = int(input("Seleccione el switch 2: "))

                self.addLink(hosts[pos_s1 - 1], switches[pos_s2 - 1])

if __name__ == '__main__':
    setLogLevel('info')
    simpleTest()
    topo = SingleLoopTopo()
    net = Mininet(topo=topo,
            controller=None,
            autoStaticArp=True)
    net.addController("c0",
            controller=RemoteController,
            ip=REMOTE_CONTROLLER_IP,
            port=6633)
    net.start()
    CLI(net)
    net.stop()