# Traffic Light Simulation

A Python-based traffic light and intersection simulation system for modeling traffic flow and analyzing waiting times.

## Overview

This project simulates traffic patterns at intersections with configurable traffic lights, vehicle arrival rates, and timing patterns. It can be used to analyze and optimize traffic flow by measuring statistics like average waiting time, maximum waiting time, and other metrics.

## Features

- Four-way intersection simulation with configurable traffic light cycles
- Customizable traffic light phases and timings
- Vehicle arrival rate modeling using exponential distribution
- Time-of-day traffic patterns (morning rush, evening rush, normal, night)
- Statistical analysis of waiting times and throughput
- Visualization of simulation results

## Project Structure

```
traffic-lights/
├── sim/
│   ├── __init__.py
│   ├── __main__.py
│   ├── intersection.py                     # Core simulation logic
│   ├── basic_fourway_intersection.py       # Sample intersection configuration
│   ├── traffic_patterns.py                 # Time-of-day traffic patterns
│   └── models/
│       ├── __init__.py
│       ├── lights.py                       # Traffic light models
│       ├── vehicles.py                     # Vehicle models
│       └── metrics.py                      # Statistics collection
├── tests/
├── .gitignore
├── AGENTS.md
├── README.md                               # <-- You are here
├── pyproject.toml                          # Currently, a single ruff rule
└── requirements.txt                        # dependencies
```

## Getting Started

### Setup


1. Clone the repository and `cd` into it:
   ``` bash
   git clone https://github.com/VLAW1/traffic-lights.git
   cd traffic-lights
   ```

2. Create a virtual environment and install the required dependencies:
   ``` bash
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Running a Simulation

Run the default four-way intersection simulation:

``` bash
python -m sim
```

You can override parameters directly on the command line:

``` bash
python -m sim --duration 7200 \
    --north-rate 0.05 --south-rate 0.05 \
    --east-rate 0.08 --west-rate 0.07 \
    --metrics-path results.json
```

## Creating Custom Intersections

You can create custom intersections by defining light configurations and phases:

``` python
from sim.models import (
    Direction,
    TrafficLightState,
    TrafficLight,
    TrafficLightCycleTime,
    Phase,
    Intersection,
)

# Define traffic lights
lights = {
    Direction.NORTH: TrafficLight(
        source=Direction.NORTH,
        destination=Direction.SOUTH,
        state=TrafficLightState.RED,
        name="North_Bound",
    ),
    # Define other lights...
}

# Define cycle times
cycle_time = TrafficLightCycleTime(green=30, yellow=3)
# Define other cycle times...

# Define traffic light phases
phases = [
    Phase(
        lights=[
            lights[Direction.NORTH],
            lights[Direction.SOUTH],
        ],
        cycle_time=cycle_time
    ),
    # Define other phases...
]

# Create intersection
intersection = Intersection(lights=lights, phases=phases)
```

## What's a "phase"?

A traffic signal "phase" is a stage of (one or more) traffic light colors. In this project, phases are defined according to which light(s) are in sync, along with the green and yellow signal durations (and are red otherwise).

(The _Manual on Uniform Traffic Control Devices_ defines a "Signal Phase" as:

> the right-of-way, yellow change, and red clearance intervals in a cycle that are assigned to an independent traffic movement or combination of movements.

See [here](https://mutcd.fhwa.dot.gov/pdfs/11th_Edition/part1.pdf), page 26. As of the time of writing, the current edition of the full manual can be found [here](https://mutcd.fhwa.dot.gov/kno_11th_Edition.htm).)

## Traffic Patterns

The system supports different traffic patterns based on time of day:

- Morning rush (7:00-9:00)
- Evening rush (16:00-18:00)
- Normal daytime
- Night (23:00-5:00)

## Output Metrics

The simulation provides the following metrics:

- Total number of vehicles processed
- Average waiting time
- Maximum and minimum waiting times
- Median waiting time
- Standard deviation of waiting times
- Optionally, a histogram visualization of waiting time distribution

## License

This project is licensed under the MIT License.