from pydantic import BaseModel
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


class Intersection(BaseModel):
    lights: dict[Direction, TrafficLight]
    phases: list[Phase]  # list[tuple[str, str]]
