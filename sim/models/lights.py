"""Core traffic light and intersection models."""

from pydantic import BaseModel, Field
from enum import StrEnum


class TrafficLightState(StrEnum):
    """Enumeration of possible traffic light colors."""
    GREEN = 'Green'
    YELLOW = 'Yellow'
    RED = 'Red'


class Direction(StrEnum):
    """Cardinal directions for traffic flow."""
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'

    def opposite(self) -> 'Direction':
        """Return the opposite cardinal direction."""
        return {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST,
        }[self]


class TrafficLight(BaseModel):
    """A single traffic light controlling movement between two directions."""
    source: Direction
    destination: Direction
    state: TrafficLightState = TrafficLightState.RED
    name: str | None = None


class TrafficLightCycleTime(BaseModel):
    """Duration of green and yellow light phases in seconds."""

    green: float
    yellow: float


class Phase(BaseModel):
    """A collection of lights that change state together."""

    lights: list[TrafficLight]
    cycle_time: TrafficLightCycleTime


class Lane(BaseModel):
    """A single movement lane controlled by a traffic light."""

    light: TrafficLight
    name: str | None = None
    queue: list[tuple[int, float]] = Field(default_factory=list)

    @property
    def source(self) -> Direction:
        return self.light.source

    @property
    def destination(self) -> Direction:
        return self.light.destination


class Intersection(BaseModel):
    """Container for lights, phases and lanes at an intersection."""

    lights: dict[Direction, TrafficLight]
    phases: list[Phase]
    lanes: dict[Direction, list[Lane]] | None = None

    @classmethod
    def create_basic_four_way(
        cls,
        cycle_time: TrafficLightCycleTime,
        *,
        light_state: TrafficLightState = TrafficLightState.RED,
    ) -> 'Intersection':
        """Return a standard four-way intersection using ``cycle_time`` for each phase."""

        lights = {
            d: TrafficLight(
                source=d,
                destination=d.opposite(),
                state=light_state,
                name=f'{d.value}_Bound',
            )
            for d in Direction
        }

        phases = [
            Phase(
                lights=[lights[Direction.NORTH], lights[Direction.SOUTH]],
                cycle_time=cycle_time,
            ),
            Phase(
                lights=[lights[Direction.EAST], lights[Direction.WEST]],
                cycle_time=cycle_time,
            ),
        ]

        lanes = {d: [Lane(light=lights[d])] for d in Direction}

        return cls(lights=lights, phases=phases, lanes=lanes)
