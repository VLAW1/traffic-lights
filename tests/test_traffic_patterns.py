import pytest
from datetime import time

from sim.traffic_patterns import TrafficPatternManager, TrafficPattern
from sim.models.lights import Direction


@pytest.fixture
def traffic_manager():
    """Return a ``TrafficPatternManager`` with fixed base rates for testing.

    Returns
    -------
    TrafficPatternManager
        Manager instance configured with constant arrival rates.
    """
    base_rates = {
        Direction.NORTH: 0.1,
        Direction.SOUTH: 0.2,
        Direction.EAST: 0.15,
        Direction.WEST: 0.25,
    }
    return TrafficPatternManager(base_rates)


class TestTrafficPatternManager:
    """Unit tests for :class:`TrafficPatternManager`."""
    def test_morning_rush_pattern(self, traffic_manager):
        """Traffic pattern should be morning rush during the early morning.

        Parameters
        ----------
        traffic_manager : TrafficPatternManager
            Instance under test.
        """
        assert (
            traffic_manager.get_pattern(time(7, 30))
            == TrafficPattern.MORNING_RUSH
        )
        assert (
            traffic_manager.get_pattern(time(8, 0))
            == TrafficPattern.MORNING_RUSH
        )
        assert (
            traffic_manager.get_pattern(time(9, 0))
            == TrafficPattern.MORNING_RUSH
        )

    def test_evening_rush_pattern(self, traffic_manager):
        """Traffic pattern should be evening rush late in the day.

        Parameters
        ----------
        traffic_manager : TrafficPatternManager
            Instance under test.
        """
        assert (
            traffic_manager.get_pattern(time(16, 0))
            == TrafficPattern.EVENING_RUSH
        )
        assert (
            traffic_manager.get_pattern(time(17, 30))
            == TrafficPattern.EVENING_RUSH
        )
        assert (
            traffic_manager.get_pattern(time(18, 0))
            == TrafficPattern.EVENING_RUSH
        )

    def test_night_pattern(self, traffic_manager):
        """Traffic pattern should switch to night in late night hours.

        Parameters
        ----------
        traffic_manager : TrafficPatternManager
            Instance under test.
        """
        assert (
            traffic_manager.get_pattern(time(23, 30)) == TrafficPattern.NIGHT
        )
        assert traffic_manager.get_pattern(time(0, 15)) == TrafficPattern.NIGHT
        assert traffic_manager.get_pattern(time(4, 45)) == TrafficPattern.NIGHT

    def test_normal_pattern(self, traffic_manager):
        """Normal pattern should be selected outside rush and night periods.

        Parameters
        ----------
        traffic_manager : TrafficPatternManager
            Instance under test.
        """
        assert (
            traffic_manager.get_pattern(time(10, 0)) == TrafficPattern.NORMAL
        )
        assert (
            traffic_manager.get_pattern(time(14, 30)) == TrafficPattern.NORMAL
        )
        assert (
            traffic_manager.get_pattern(time(20, 0)) == TrafficPattern.NORMAL
        )

    def test_morning_rush_rates(self, traffic_manager):
        """Arrival rates double during the morning rush.

        Parameters
        ----------
        traffic_manager : TrafficPatternManager
            Instance under test.
        """
        rates = traffic_manager.get_arrival_rates(time(8, 0))
        assert rates[Direction.NORTH] == pytest.approx(0.2)  # 0.1 * 2.0
        assert rates[Direction.SOUTH] == pytest.approx(0.4)  # 0.2 * 2.0
        assert rates[Direction.EAST] == pytest.approx(0.3)  # 0.15 * 2.0
        assert rates[Direction.WEST] == pytest.approx(0.5)  # 0.25 * 2.0

    def test_evening_rush_rates(self, traffic_manager):
        """Arrival rates increase during the evening rush.

        Parameters
        ----------
        traffic_manager : TrafficPatternManager
            Instance under test.
        """
        rates = traffic_manager.get_arrival_rates(time(17, 0))
        assert rates[Direction.NORTH] == pytest.approx(0.18)  # 0.1 * 1.8
        assert rates[Direction.SOUTH] == pytest.approx(0.36)  # 0.2 * 1.8
        assert rates[Direction.EAST] == pytest.approx(0.27)  # 0.15 * 1.8
        assert rates[Direction.WEST] == pytest.approx(0.45)  # 0.25 * 1.8

    def test_normal_rates(self, traffic_manager):
        """Base arrival rates are returned during normal periods.

        Parameters
        ----------
        traffic_manager : TrafficPatternManager
            Instance under test.
        """
        rates = traffic_manager.get_arrival_rates(time(12, 0))
        assert rates[Direction.NORTH] == pytest.approx(0.1)  # 0.1 * 1.0
        assert rates[Direction.SOUTH] == pytest.approx(0.2)  # 0.2 * 1.0
        assert rates[Direction.EAST] == pytest.approx(0.15)  # 0.15 * 1.0
        assert rates[Direction.WEST] == pytest.approx(0.25)  # 0.25 * 1.0

    def test_night_rates(self, traffic_manager):
        """Arrival rates are reduced during the night.

        Parameters
        ----------
        traffic_manager : TrafficPatternManager
            Instance under test.
        """
        rates = traffic_manager.get_arrival_rates(time(1, 0))
        assert rates[Direction.NORTH] == pytest.approx(0.03)  # 0.1 * 0.3
        assert rates[Direction.SOUTH] == pytest.approx(0.06)  # 0.2 * 0.3
        assert rates[Direction.EAST] == pytest.approx(0.045)  # 0.15 * 0.3
        assert rates[Direction.WEST] == pytest.approx(0.075)  # 0.25 * 0.3
