import pandas as pd
from pathlib import Path

from sim.intersection import simulate
import numpy as np
from sim.basic_fourway_intersection import intersection, arrival_rates
from sim.traffic_patterns import TrafficPatternManager


def test_to_csv(tmp_path):
    np.random.seed(42)
    manager = TrafficPatternManager(arrival_rates)
    stats = simulate(100, intersection, traffic_manager=manager, start_time=0)
    output = tmp_path / "out.csv"
    stats.to_csv(output)

    expected_path = Path(__file__).with_name("test.csv")
    df_expected = pd.read_csv(expected_path)
    df_actual = pd.read_csv(output)
    pd.testing.assert_frame_equal(df_actual, df_expected)
