"""Command line interface for running traffic light simulations."""

import argparse
import json
from pathlib import Path

from sim.basic_fourway_intersection import (
    arrival_rates as default_rates,
    duration as default_duration,
    intersection,
)
from sim.intersection import simulate
from sim.models.lights import Direction


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed arguments populated with defaults from
        :mod:`sim.basic_fourway_intersection`.
    """

    parser = argparse.ArgumentParser(description='Traffic light simulation')
    parser.add_argument(
        '--duration',
        type=int,
        default=default_duration,
        help='Simulation duration in seconds',
    )
    parser.add_argument(
        '--north-rate',
        type=float,
        default=default_rates[Direction.NORTH],
        help='Northbound arrival rate (vehicles/sec)',
    )
    parser.add_argument(
        '--south-rate',
        type=float,
        default=default_rates[Direction.SOUTH],
        help='Southbound arrival rate (vehicles/sec)',
    )
    parser.add_argument(
        '--east-rate',
        type=float,
        default=default_rates[Direction.EAST],
        help='Eastbound arrival rate (vehicles/sec)',
    )
    parser.add_argument(
        '--west-rate',
        type=float,
        default=default_rates[Direction.WEST],
        help='Westbound arrival rate (vehicles/sec)',
    )
    parser.add_argument(
        '--metrics-path',
        type=Path,
        help='Path to write summary metrics as JSON',
    )
    return parser.parse_args()


def main() -> None:
    """Run the simulation with parameters from ``parse_args``."""

    args = parse_args()
    rates = {
        Direction.NORTH: args.north_rate,
        Direction.SOUTH: args.south_rate,
        Direction.EAST: args.east_rate,
        Direction.WEST: args.west_rate,
    }

    stats = simulate(args.duration, intersection, rates)
    stats.show_summary()

    if args.metrics_path:
        args.metrics_path.write_text(json.dumps(stats.to_dict(), indent=2))


if __name__ == '__main__':
    main()
