from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

from dataclasses import dataclass

from vessel import *
import random
import numpy as np

# Average amount of vessels arriving at the port on an hourly basis
NUM_VESSELS_ARRIVING_PER_HOUR = [100, 120, 150, 175, 125, 50, 42, 68, 200, 220, 250, 245, 253, 236, 227, 246, 203, 43,
                                 51, 33, 143, 187, 164, 123]
SECONDS_PER_HOUR = 3600
HOURS_PER_DAY = 24


@dataclass
class GeneratorState:
    # Remaining time until generation of new event
    remaining: float = 0.0
    # Current simulation time
    current_time: float = 0.0

    last_vessel_number_in_current_hour: int = 0


class Generator(AtomicDEVS):
    def __init__(self, name):
        super(Generator, self).__init__(name)
        self.out = self.addOutPort("out")
        self.state = GeneratorState()

    def intTransition(self):
        # Compute the hour, before the time advance
        old_hour = int(self.state.current_time) // SECONDS_PER_HOUR + 1

        # Update simulation time
        self.state.current_time += self.timeAdvance()

        # Find the index of the bar chart
        hour = int(self.state.current_time) // SECONDS_PER_HOUR + 1
        mod_hour = hour % HOURS_PER_DAY

        if hour != old_hour:
            self.state.last_vessel_number_in_current_hour = 1
        else:
            self.state.last_vessel_number_in_current_hour += 1

        # Index the bar chart
        num_vessels = NUM_VESSELS_ARRIVING_PER_HOUR[mod_hour]

        # Compute the Inter-Arrival-Time
        iat = np.random.gamma(self.state.last_vessel_number_in_current_hour, 1 / num_vessels)
        iat = iat * (2/num_vessels) * SECONDS_PER_HOUR # rescale
        self.state.remaining = iat

        return self.state

    def timeAdvance(self):
        # Return remaining time
        return self.state.remaining

    def outputFnc(self):
        # Sample vessel type
        weights = [vessel.prob for vessel in ALL_VESSELS]
        chosen_vessel_obj = random.choices(ALL_VESSELS, weights=weights)[0]
        return {self.out: chosen_vessel_obj()}
