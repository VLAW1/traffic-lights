"""Vehicle related types and utilities."""

from sim.models.lights import Direction


ArrivalRates = dict[Direction, float]
"""Type alias for per-direction arrival rates."""
