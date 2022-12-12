from pypdevs.simulator import Simulator
from pypdevs.DEVS import AtomicDEVS, CoupledDEVS

from messages import PortEntryRequest
from control_tower import ControlTower


# A simple generator that sends PortEntryRequest every second
class SimpleGenerator(AtomicDEVS):
    def __init__(self, name):
        super(SimpleGenerator, self).__init__(name)

        # Sends PortEntryRequest's
        self.out_port_entry_request = self.addOutPort("out_port_entry_request")

        # Define the state
        self.count = 0

    def intTransition(self):
        self.count += 1
        return self.count

    def timeAdvance(self):
        return 1.0

    def outputFnc(self):
        port_entry_request = PortEntryRequest(
            vessel_uid=self.count
        )
        return {self.out_port_entry_request: port_entry_request}


# A simple collector that receives PortEntryPermission's from ControlTower
class SimpleCollector(AtomicDEVS):
    def __init__(self, name):
        super(SimpleCollector, self).__init__(name)

        # Receives PortEntryPermission's
        self.in_port_entry_permission = self.addInPort("in_port_entry_permission")

        # Collects PortEntryPermission's
        # Acts as the state
        self.port_entry_permissions = []

    def extTransition(self, inputs):
        if self.in_port_entry_permission in inputs:
            port_entry_permission = inputs[self.in_port_entry_permission]
            self.port_entry_permissions.append(port_entry_permission)
        return self.port_entry_permissions


class CoupledControlTower(CoupledDEVS):
    def __init__(self, name):
        super(CoupledControlTower, self).__init__(name)

        self.simple_generator = self.addSubModel(SimpleGenerator("simple_generator"))
        self.control_tower = self.addSubModel(ControlTower("control_tower"))
        self.simple_collector = self.addSubModel(SimpleCollector("simple_collector"))

        self.connectPorts(self.simple_generator.out_port_entry_request, self.control_tower.in_port_entry_request)
        self.connectPorts(self.control_tower.out_port_entry_permission, self.simple_collector.in_port_entry_permission)


system = CoupledControlTower(name="system")
sim = Simulator(system)
sim.setTerminationTime(4)
sim.setVerbose(None)
sim.setClassicDEVS()

sim.simulate()

# should be
# [
#   PortEntryPermission(vessel_uid=0, avl_dock='1'),
#   PortEntryPermission(vessel_uid=1, avl_dock='2'),
#   PortEntryPermission(vessel_uid=2, avl_dock='3'),
#   PortEntryPermission(vessel_uid=3, avl_dock='4')
# ]
print(system.simple_collector.port_entry_permissions)