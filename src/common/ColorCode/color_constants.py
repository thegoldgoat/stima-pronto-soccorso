from src.simulator.generators.exponential_generator import ExponentialGenerator
from src.simulator.generators.gauss_generator import GaussGenerator

COLOR_RED = 0
COLOR_YELLOW = 1
COLOR_GREEN = 2

COLORS = [COLOR_RED, COLOR_YELLOW, COLOR_GREEN]

# For interarrivals
COLOR_RATES = [
    # Red
    20,
    # Yellow
    10,
    # Green
    3
]

# To generate therapy time based on interarrival patients color code
COLOR_GAUSSIANS = [
    GaussGenerator(10, 4),
    GaussGenerator(7, 3),
    GaussGenerator(4, 2)
]

# To generate leave time based on interarrival patients color code
COLOR_LEAVE = [
    ExponentialGenerator(0.00001),
    ExponentialGenerator(0.001),
    ExponentialGenerator(0.1)
]
