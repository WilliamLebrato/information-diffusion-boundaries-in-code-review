import timeit
import unittest
from simulation.model import CommunicationNetwork
from simulation.run import run_simulation, argparse
from unittest.mock import patch
import pstats


class TestPerformance(unittest.TestCase):
    @unittest.skip("Performance test is skipped due to the long execution time")
    def test_performance_time(self):
        start_time = timeit.default_timer()
        run_simulation()
        end_time = timeit.default_timer()
        print(f"Execution time: {end_time - start_time} seconds")
        p = pstats.Stats('outputfile')
        p.sort_stats('cumulative').print_stats(20)



# class TestArguments(unittest.TestCase):
#     @patch('argparse.ArgumentParser.parse_args',
#            return_value=argparse.Namespace(param1="value1", param2="value2"))
#     def test_argument_parsing(self):
#         args = run_simulation()
#         self.assertEqual(args.param1, "value1")
#         self.assertEqual(args.param2, "value2")

if __name__ == "__main__":
    unittest.main()