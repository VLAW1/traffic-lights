"""Collection of utilities for measuring simulation performance."""

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from pydantic import ConfigDict
from pydantic.dataclasses import dataclass, Field
import pandas as pd
from pathlib import Path


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class SummaryStatistics:
    """Statistics collected during a simulation run."""

    total_vehicles: int = 0
    waiting_times: npt.ArrayLike = Field(default_factory=lambda: np.array([]))

    def average_waiting_time(self):
        """Return the mean waiting time for all vehicles."""

        if self.total_vehicles == 0:
            return 0.0
        return sum(self.waiting_times) / self.total_vehicles

    def max_waiting_time(self):
        """Return the maximum waiting time observed."""

        if len(self.waiting_times) == 0:
            return 0.0
        return max(self.waiting_times)

    def min_waiting_time(self):
        """Return the minimum waiting time observed."""

        if len(self.waiting_times) == 0:
            return 0.0
        return min(self.waiting_times)

    def median_waiting_time(self):
        """Return the median waiting time."""

        return np.median(self.waiting_times)

    def standard_deviation_waiting_time(self):
        """Return the standard deviation of waiting times."""

        return np.std(self.waiting_times)

    def variance_waiting_time(self):
        """Return the variance of waiting times."""

        return np.var(self.waiting_times)

    def total_waiting_time(self):
        """Return the sum of all waiting times."""

        return sum(self.waiting_times)

    def plot_waiting_times(self):
        """Display a histogram of waiting times."""

        plt.hist(self.waiting_times)
        plt.show()

    def to_dict(self) -> dict:
        """Return summary statistics as a serializable dictionary."""
        return {
            'total_vehicles': self.total_vehicles,
            'average_waiting_time': self.average_waiting_time(),
            'max_waiting_time': self.max_waiting_time(),
            'min_waiting_time': self.min_waiting_time(),
            'median_waiting_time': self.median_waiting_time(),
            'std_waiting_time': self.standard_deviation_waiting_time(),
            'variance_waiting_time': self.variance_waiting_time(),
            'total_waiting_time': self.total_waiting_time(),
        }

    def to_csv(self, file_path: str | Path) -> None:
        """Write the summary statistics to ``file_path`` as CSV.

        Parameters
        ----------
        file_path : str | Path
            Destination CSV path. Any parent directories must already exist.
        """

        df = pd.DataFrame([self.to_dict()])
        df.to_csv(Path(file_path), index=False)

    def show_summary(self, include_plot: bool = False):
        """Print a formatted summary of all metrics."""

        print(
            f'Total vehicles:           {self.total_vehicles:.2f}\n'
            f'Average waiting time:     {self.average_waiting_time():.2f}\n'
            f'Max waiting time:         {self.max_waiting_time():.2f}\n'
            f'Min waiting time:         {self.min_waiting_time():.2f}\n'
            f'Median waiting time:      {self.median_waiting_time():.2f}\n'
            f'Std waiting time:         {self.standard_deviation_waiting_time():.2f}\n'
            f'Variance waiting time:    {self.variance_waiting_time():.2f}\n'
            f'Total waiting time:       {self.total_waiting_time():.2f}'
        )

        if include_plot:
            self.plot_waiting_times()
