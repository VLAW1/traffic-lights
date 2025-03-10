from sim.models import (
    Direction,
    TrafficLightState,
    TrafficLight,
    TrafficLightCycleTime,
    Phase,
    Intersection,
)


lights = {
    Direction.NORTH: TrafficLight(
        source=Direction.NORTH,
        destination=Direction.SOUTH,
        state=TrafficLightState.RED,
        name='North_Bound',
    ),
    Direction.SOUTH: TrafficLight(
        source=Direction.SOUTH,
        destination=Direction.NORTH,
        state=TrafficLightState.RED,
        name='South_Bound',
    ),
    Direction.EAST: TrafficLight(
        source=Direction.EAST,
        destination=Direction.WEST,
        state=TrafficLightState.RED,
        name='East_Bound',
    ),
    Direction.WEST: TrafficLight(
        source=Direction.WEST,
        destination=Direction.EAST,
        state=TrafficLightState.RED,
        name='West_Bound',
    ),
}

uniform_cyle_time = TrafficLightCycleTime(
    green=30,
    yellow=3,
)

phases = [
    Phase(
        lights=[
            lights[Direction.NORTH],
            lights[Direction.SOUTH],
        ],
        cycle_time=uniform_cyle_time,
    ),
    Phase(
        lights=[
            lights[Direction.EAST],
            lights[Direction.WEST],
        ],
        cycle_time=uniform_cyle_time,
    ),
]


intersection: Intersection = Intersection(lights=lights, phases=phases)


# Vehicle arrival rates (vehicles/sec)
arrival_rates = {
    Direction.NORTH: 0.05,
    Direction.EAST: 0.08,
    Direction.SOUTH: 0.05,
    Direction.WEST: 0.07,
}


duration: int = 3600  # seconds
