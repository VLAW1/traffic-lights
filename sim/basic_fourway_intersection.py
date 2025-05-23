"""Default four-way intersection configuration for examples and tests."""

from sim.models import (
    Direction,
    TrafficLightCycleTime,
    Intersection,
)


uniform_cyle_time = TrafficLightCycleTime(green=30, yellow=3)
intersection: Intersection = Intersection.create_basic_four_way(uniform_cyle_time)


arrival_rates = {
    Direction.NORTH: 0.05,
    Direction.EAST: 0.08,
    Direction.SOUTH: 0.05,
    Direction.WEST: 0.07,
}
"""Default per-direction arrival rates in vehicles per second."""


duration: int = 3600
"""Default simulation duration in seconds."""
