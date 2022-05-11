from src.simulator.generators.exponential_generator import ExponentialGenerator
from src.simulator.generators.gauss_generator import GaussGenerator

THERAPY_SIZE = 7

ESI_CODES = [1,2,3,4,5]

# For interarrivals
ESI_RATES = [
    # 1
    100,
    # 2
    80,
    # 3
    30,
    # 4
    20,
    # 5
    10
]

# To generate therapy time based on interarrival patients esi code
ESI_GAUSSIANS = [
    # 1
    GaussGenerator(8, 4),
    # 2
    GaussGenerator(7, 3),
    # 3
    GaussGenerator(6, 2),
    # 4
    GaussGenerator(5, 3),
    # 5
    GaussGenerator(4, 2)
]

# To generate leave time based on interarrival patients esi code
ESI_LEAVE = [
    # 1
    ExponentialGenerator(0.00001),
    # 2
    ExponentialGenerator(0.00001),
    # 3
    ExponentialGenerator(0.00001),
    # 4
    ExponentialGenerator(0.001),
    # 5
    ExponentialGenerator(0.1)
]
