from pypdevs.simulator import Simulator
from generator import Generator

system = Generator(name="system")
sim = Simulator(system)
# simulate 1 hour
sim.setTerminationTime(3600.0)
sim.setVerbose(None)
sim.setClassicDEVS()

sim.simulate()

# should be around 100
# that is, the first index of the bar chart
print(f"number of vessels generated: {system.state.vessel_count}")