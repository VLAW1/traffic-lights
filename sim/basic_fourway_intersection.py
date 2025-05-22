from sim.models import (
    Direction,
    TrafficLightCycleTime,
    Intersection,
)


uniform_cyle_time = TrafficLightCycleTime(green=30, yellow=3)

# Create a standard four-way intersection using the cycle time above.
intersection: Intersection = Intersection.create_basic_four_way(uniform_cyle_time)


# Vehicle arrival rates (vehicles/sec)
arrival_rates = {
    Direction.NORTH: 0.05,
    Direction.EAST: 0.08,
    Direction.SOUTH: 0.05,
    Direction.WEST: 0.07,
}


duration: int = 3600  # seconds
