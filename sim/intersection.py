from collections.abc import Generator
from itertools import cycle
from typing import Any
import random
from datetime import datetime, timedelta

from sim.traffic_patterns import TrafficPatternManager

import simpy
import numpy as np

from sim.models import (
    Direction,
    TrafficLight,
    TrafficLightState,
    Intersection,
    Lane,
    ArrivalRates,
    SummaryStatistics,
)

np.random.seed(42)


class IntersectionSimulation:
    def __init__(self, env, intersection: Intersection) -> None:
        self.env = env
        self.lights = intersection.lights
        self.phase_cycle = cycle(intersection.phases)
        self.lanes = intersection.lanes or {}
        self.stats = SummaryStatistics()

        # start the traffic light cycle
        env.process(self.run())

    def change_lights(self, lights: list[TrafficLight], state: TrafficLightState):
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
        lane: Lane,
    ) -> Generator[Any, Any, None]:
        arrival_time = self.env.now
        self.stats.total_vehicles += 1
        lane.queue.append((vehicle_id, arrival_time))
        # wait until light is green and vehicle is next up in queue
        while True:
            if (
                lane.light.state == TrafficLightState.GREEN
                and lane.queue[0][0] == vehicle_id
            ):
                waiting_time = self.env.now - arrival_time
                self.stats.waiting_times = np.append(
                    self.stats.waiting_times, waiting_time
                )
                lane.queue.pop(0)
                break
            yield self.env.timeout(1)


def generate_vehicle_arrivals(
    env,
    intersection_sim: IntersectionSimulation,
    direction: Direction,
    rate: float,
    traffic_manager: 'TrafficPatternManager | None' = None,
):
    vehicle_id = 0
    while True:
        # determine the current arrival rate
        current_rate = rate
        if traffic_manager is not None:
            # convert current simulation time to a time-of-day value
            seconds = int(env.now) % (24 * 60 * 60)
            current_time = (datetime.min + timedelta(seconds=seconds)).time()
            current_rate = traffic_manager.get_arrival_rates(current_time)[direction]

        # np.random.exponential expects the scale (1/lambda). `current_rate` is
        # the arrival rate (lambda) in vehicles per second, so we convert it to
        # the mean inter-arrival time.
        yield env.timeout(np.random.exponential(1 / current_rate))
        # spawn vehicle
        vehicle_id += 1
        lanes = intersection_sim.lanes.get(direction)
        if lanes:
            lane = random.choice(lanes)
        else:
            lane = Lane(light=intersection_sim.lights[direction])
        env.process(intersection_sim.vehicle_arrival(vehicle_id, lane))


def simulate(
    duration: int,
    intersection: Intersection,
    arrival_rates: ArrivalRates | None = None,
    *,
    traffic_manager: 'TrafficPatternManager | None' = None,
    start_time: int = 0,
) -> SummaryStatistics:
    env = simpy.Environment(initial_time=start_time)

    # start intersection simulation
    intersection_sim = IntersectionSimulation(env, intersection)

    # start vehicle arrival processes
    if traffic_manager is not None:
        base_rates = traffic_manager.base_rates
        for direction, rate in base_rates.items():
            env.process(
                generate_vehicle_arrivals(
                    env,
                    intersection_sim,
                    direction,
                    rate,
                    traffic_manager,
                )
            )
    elif arrival_rates is not None:
        for direction, rate in arrival_rates.items():
            env.process(
                generate_vehicle_arrivals(env, intersection_sim, direction, rate)
            )
    else:
        raise ValueError('Either arrival_rates or traffic_manager must be provided')

    # run simulation
    env.run(until=duration)

    return intersection_sim.stats
