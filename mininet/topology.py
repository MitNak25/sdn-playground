import os
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.topo import Topo
from mininet.cli import CLI


class SimpleTopo(Topo):
    def build(self):
        switch = self.addSwitch('s1')
        for index in range(1, 4):
            host = self.addHost(f'h{index}', ip=f'10.0.0.{index}/24')
            self.addLink(host, switch)


if __name__ == '__main__':
    net = Mininet(topo=SimpleTopo(), switch=OVSKernelSwitch, controller=None, autoSetMacs=True)
    net.addController('c0', controller=RemoteController, ip=os.getenv('RYU_HOST', '127.0.0.1'), port=6633)
    net.start()
    net.pingAll()
    CLI(net)
    net.stop()
