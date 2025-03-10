from datetime import time
from enum import StrEnum

from sim.models.lights import Direction


class TrafficPattern(StrEnum):
    MORNING_RUSH = 'morning_rush'
    EVENING_RUSH = 'evening_rush'
    NORMAL = 'normal'
    NIGHT = 'night'


class TrafficPatternManager:
    def __init__(self, base_arrival_rates: dict[Direction, float]):
        self.base_rates = base_arrival_rates
        self.multipliers = {
            TrafficPattern.MORNING_RUSH: 2.0,
            TrafficPattern.EVENING_RUSH: 1.8,
            TrafficPattern.NORMAL: 1.0,
            TrafficPattern.NIGHT: 0.3,
        }

    def get_pattern(self, current_time: time) -> TrafficPattern:
        if time(7, 0) <= current_time <= time(9, 0):
            return TrafficPattern.MORNING_RUSH
        elif time(16, 0) <= current_time <= time(18, 0):
            return TrafficPattern.EVENING_RUSH
        elif time(23, 0) <= current_time or current_time <= time(5, 0):
            return TrafficPattern.NIGHT
        return TrafficPattern.NORMAL

    def get_arrival_rates(self, current_time: time) -> dict[Direction, float]:
        pattern = self.get_pattern(current_time)
        multiplier = self.multipliers[pattern]
        return {
            direction: rate * multiplier
            for direction, rate in self.base_rates.items()
        }
