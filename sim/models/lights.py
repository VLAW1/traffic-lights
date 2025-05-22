from pydantic import BaseModel, Field
from enum import StrEnum


class TrafficLightState(StrEnum):
    GREEN = 'Green'
    YELLOW = 'Yellow'
    RED = 'Red'


class Direction(StrEnum):
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'


class TrafficLight(BaseModel):
    source: Direction
    destination: Direction
    state: TrafficLightState = TrafficLightState.RED
    name: str | None = None


# Traffice light cycle times model
class TrafficLightCycleTime(BaseModel):
    green: float
    yellow: float


# "phase" := synchronized light combinations
class Phase(BaseModel):
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
    lights: dict[Direction, TrafficLight]
    phases: list[Phase]  # list[tuple[str, str]]
    lanes: dict[Direction, list[Lane]] | None = None
