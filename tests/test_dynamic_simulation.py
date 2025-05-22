import numpy as np
import simpy
import pytest
from datetime import time

from sim.basic_fourway_intersection import intersection
from sim.intersection import (
    IntersectionSimulation,
    generate_vehicle_arrivals,
)
from sim.models.lights import Direction
from sim.traffic_patterns import TrafficPatternManager


def run_single_direction(start_time: time, multiplier: float, monkeypatch):
    base_rate = 0.2
    manager = TrafficPatternManager({Direction.NORTH: base_rate})
    scales = []
    orig_exp = np.random.exponential

    def recording_exp(scale):
        scales.append(scale)
        return orig_exp(scale)

    monkeypatch.setattr(np.random, 'exponential', recording_exp)
    seconds = start_time.hour * 3600 + start_time.minute * 60 + start_time.second
    env = simpy.Environment(initial_time=seconds)
    sim = IntersectionSimulation(env, intersection)
    env.process(
        generate_vehicle_arrivals(env, sim, Direction.NORTH, base_rate, manager)
    )
    env.run(until=seconds + 1)
    assert scales[0] == pytest.approx(1 / (base_rate * multiplier))


@pytest.mark.parametrize(
    'start, multiplier',
    [
        (time(8, 0), 2.0),
        (time(17, 0), 1.8),
        (time(12, 0), 1.0),
        (time(1, 0), 0.3),
    ],
)
def test_dynamic_rate(monkeypatch, start, multiplier):
    run_single_direction(start, multiplier, monkeypatch)


def test_rate_changes_with_time(monkeypatch):
    base_rate = 0.1
    manager = TrafficPatternManager({Direction.NORTH: base_rate})
    scales = []

    def fixed_exp(scale):
        scales.append(scale)
        return 1

    monkeypatch.setattr(np.random, 'exponential', fixed_exp)
    start_seconds = 8 * 3600 + 59 * 60 + 59
    env = simpy.Environment(initial_time=start_seconds)
    sim = IntersectionSimulation(env, intersection)
    env.process(
        generate_vehicle_arrivals(env, sim, Direction.NORTH, base_rate, manager)
    )
    env.run(until=start_seconds + 3)
    assert scales[0] == pytest.approx(1 / (base_rate * 2.0))
    assert scales[1] == pytest.approx(1 / (base_rate * 2.0))
    assert scales[2] == pytest.approx(1 / base_rate)
