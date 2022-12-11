from pypdevs.simulator import Simulator
from generator import Generator

system = Generator(name="system")
sim = Simulator(system)
sim.setTerminationTime(400.0)
sim.setVerbose(None)
sim.setClassicDEVS()

sim.simulate()

