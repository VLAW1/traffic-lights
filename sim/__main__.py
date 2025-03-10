from sim.intersection import simulate
from sim.basic_fourway_intersection import intersection, arrival_rates

stats = simulate(1000, intersection, arrival_rates)

stats.show_summary()
