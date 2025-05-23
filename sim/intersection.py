"""Simulation engine for traffic light intersections."""

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
    """Manage the state of an ``Intersection`` in a ``simpy`` environment."""

    def __init__(self, env, intersection: Intersection) -> None:
        """Initialize the simulation and start the light cycle."""

        self.env = env
        self.lights = intersection.lights
        self.phase_cycle = cycle(intersection.phases)
        self.lanes = intersection.lanes or {}
        self.stats = SummaryStatistics()

        env.process(self.run())

    def change_lights(self, lights: list[TrafficLight], state: TrafficLightState) -> None:
        """Set ``state`` on all traffic ``lights``."""

        for light in lights:
            self.lights[light.source].state = state

    def run(self) -> Generator[Any, Any, None]:
        """Iterate through the configured phases indefinitely."""

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
        """Process a single vehicle through ``lane``."""

        arrival_time = self.env.now
        self.stats.total_vehicles += 1
        lane.queue.append((vehicle_id, arrival_time))
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
    """Yield vehicle arrival events according to ``rate`` or a manager."""

    vehicle_id = 0
    while True:
        current_rate = rate
        if traffic_manager is not None:
            seconds = int(env.now) % (24 * 60 * 60)
            current_time = (datetime.min + timedelta(seconds=seconds)).time()
            current_rate = traffic_manager.get_arrival_rates(current_time)[direction]

        # ``numpy.random.exponential`` expects a scale of ``1/lambda``.
        yield env.timeout(np.random.exponential(1 / current_rate))
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
    """Run a complete intersection simulation.

    Parameters
    ----------
    duration : int
        Length of the simulation in seconds.
    intersection : Intersection
        Intersection configuration to simulate.
    arrival_rates : ArrivalRates | None, optional
        Constant per-direction arrival rates. Ignored when
        ``traffic_manager`` is provided.
    traffic_manager : TrafficPatternManager | None, optional
        Manager used to update arrival rates dynamically.
    start_time : int, optional
        Initial simulation time in seconds.

    Returns
    -------
    SummaryStatistics
        Collected simulation statistics.
    """

    env = simpy.Environment(initial_time=start_time)

    intersection_sim = IntersectionSimulation(env, intersection)

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

    env.run(until=duration)

    return intersection_sim.stats
