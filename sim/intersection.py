from collections import defaultdict
from collections.abc import Generator
from itertools import cycle
from typing import Any
import simpy
import numpy as np

from sim.models import (
    Direction,
    TrafficLight,
    TrafficLightState,
    Intersection,
    ArrivalRates,
    SummaryStatistics,
)

np.random.seed(42)


class IntersectionSimulation:
    def __init__(self, env, intersection: Intersection) -> None:
        self.env = env
        self.lights = intersection.lights
        self.phase_cycle = cycle(intersection.phases)
        self.queues = defaultdict(list)
        self.stats = SummaryStatistics()

        # start the traffic light cycle
        env.process(self.run())

    def change_lights(
        self, lights: list[TrafficLight], state: TrafficLightState
    ):
        for light in lights:
            self.lights[light.source].state = state

    def run(self) -> Generator[Any, Any, None]:
        while True:
            next_phase = next(self.phase_cycle)
            lights = next_phase.lights

            self.change_lights(lights, TrafficLightState.GREEN)
            yield self.env.timeout(next_phase.cycle_time.green)

            self.change_lights(lights, TrafficLightState.YELLOW)
            yield self.env.timeout(next_phase.cycle_time.yellow)

            self.change_lights(lights, TrafficLightState.RED)

    def vehicle_arrival(
        self,
        vehicle_id: int,
        direction: Direction,
    ) -> Generator[Any, Any, None]:
        arrival_time = self.env.now
        self.stats.total_vehicles += 1
        self.queues[direction].append((vehicle_id, arrival_time))
        # wait until light is green and vehicle is next up in queue
        while True:
            if (
                self.lights[direction].state == TrafficLightState.GREEN
                and self.queues[direction][0][0] == vehicle_id
            ):
                waiting_time = self.env.now - arrival_time
                self.stats.waiting_times = np.append(
                    self.stats.waiting_times, waiting_time
                )
                self.queues[direction].pop(0)
                break
            yield self.env.timeout(1)


def generate_vehicle_arrivals(
    env,
    intersection_sim: IntersectionSimulation,
    direction: Direction,
    rate: float,
):
    vehicle_id = 0
    while True:
        # wait based on defined vehicle arrival rate
        yield env.timeout(np.random.exponential(rate))
        # spawn vehicle
        vehicle_id += 1
        env.process(intersection_sim.vehicle_arrival(vehicle_id, direction))


def simulate(
    duration: int, intersection: Intersection, arrival_rates: ArrivalRates
) -> SummaryStatistics:
    env = simpy.Environment()

    # start intersection simulation
    intersection_sim = IntersectionSimulation(env, intersection)

    # start vehicle arrival processes
    for direction, rate in arrival_rates.items():
        env.process(
            generate_vehicle_arrivals(env, intersection_sim, direction, rate)
        )

    # run simulation
    env.run(until=duration)

    return intersection_sim.stats
