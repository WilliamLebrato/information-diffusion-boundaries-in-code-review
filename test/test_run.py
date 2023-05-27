import timeit
import unittest
from simulation.model import CommunicationNetwork
from simulation.run import run_simulation

class TestPerformance(unittest.TestCase):
    @unittest.skip("Performance test is skipped due to the long execution time")
    def test_performance():
        start_time = timeit.default_timer()
        run_simulation()
        end_time = timeit.default_timer()
        print(f"Execution time: {end_time - start_time} seconds")

    test_performance()
