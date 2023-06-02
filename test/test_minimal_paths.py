import unittest
import simulation.model

from simulation.model import CommunicationNetwork
from simulation.minimal_paths import single_source_dijkstra_vertices, single_source_dijkstra_hyperedges, single_source_bellman_ford_hypergraph, DistanceType

class MinimalPath(unittest.TestCase):
    cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

    def test_1(self):
        self.assertEqual(single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0), {'v2': 1, 'v3': 2, 'v4': 3})

    def test_2(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_3(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.FASTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.FASTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_4(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.FOREMOST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.FOREMOST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_hypergraph_large(self):
        cn_very_large = CommunicationNetwork({f'h{i}': [f'v{j}' for j in range(100)] for i in range(100)}, {f'h{i}': i for i in range(100)})
        result_1 = single_source_dijkstra_vertices(cn_very_large, 'v1', DistanceType.SHORTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(cn_very_large, 'v1', DistanceType.SHORTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_bellman_ford_shortest_path(self):
        result_bellman_ford = single_source_bellman_ford_hypergraph(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        self.assertEqual(result_bellman_ford, {'v2': 1, 'v3': 2, 'v4': 3}, 'Bellman-Ford failed to find the shortest path')

    def test_bellman_ford_vs_dijkstra(self):
        result_bellman_ford = single_source_bellman_ford_hypergraph(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        result_dijkstra = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        self.assertEqual(result_bellman_ford, result_dijkstra, 'Bellman-Ford and Dijkstra implementations are not equivalent')

class MinimalPathExceptionHandling(unittest.TestCase):
        def test_minimal_path_unknown_vertice(self):
            cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

            with self.assertRaises(simulation.model.EntityNotFound):
                single_source_dijkstra_vertices(cn, 'v69', DistanceType.SHORTEST, min_timing=0)

            with self.assertRaises(simulation.model.EntityNotFound):
                single_source_dijkstra_hyperedges(cn, 'v69', DistanceType.SHORTEST, min_timing=0)

class TestBoundaryCases(unittest.TestCase):
    cn_empty = CommunicationNetwork({}, {})
    cn_single_vertex = CommunicationNetwork({'h1': ['v1']}, {'h1': 1})

        # For an empty graph the EntityNotFound exeption should be raised
    def test_empty_graph(self):
        with self.assertRaises(simulation.model.EntityNotFound):
            single_source_dijkstra_vertices(TestBoundaryCases.cn_empty, 'v1', DistanceType.SHORTEST, min_timing=0)
            single_source_dijkstra_hyperedges(TestBoundaryCases.cn_empty, 'v1', DistanceType.SHORTEST, min_timing=0)
    
    @unittest.expectedFailure
    def test_single_vertex(self):
        self.assertEqual(single_source_dijkstra_vertices(TestBoundaryCases.cn_single_vertex, 'v1', DistanceType.SHORTEST, min_timing=0), {'v1': 0}, 'Provided a graph of only one vertex the expected result is a dictionary with one key and the value 0.')
        self.assertEqual(single_source_dijkstra_hyperedges(TestBoundaryCases.cn_single_vertex, 'v1', DistanceType.SHORTEST, min_timing=0), {'v1': 0}, 'Provided a graph of only one vertex the expected result is a dictionary with one key and the value 0.')

class TestNegativeWeights(unittest.TestCase):
    cn_negative_weights = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': -1, 'h2': -2, 'h3': -3})

        # Dijkstras algorithm should not handle negative weights, therefore an exeption is expected.
    @unittest.expectedFailure
    def test_negative_weights(self):
        with self.assertRaises(Exception):
            single_source_dijkstra_vertices(TestNegativeWeights.cn_negative_weights, 'v1', DistanceType.SHORTEST, min_timing=0)

        with self.assertRaises(Exception):
            single_source_dijkstra_hyperedges(TestNegativeWeights.cn_negative_weights, 'v1', DistanceType.SHORTEST, min_timing=0)

class TestMultiplePaths(unittest.TestCase):
    cn_multiple_paths = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v1', 'v3']}, {'h1': 1, 'h2': 1, 'h3': 1})

        # If there are multiple shortest, fastest, or foremost paths between the source and a given vertex we want to make sure the algorithm handles these situations correctly
    def test_multiple_paths(self):
        result_1 = single_source_dijkstra_vertices(TestMultiplePaths.cn_multiple_paths, 'v1', DistanceType.SHORTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(TestMultiplePaths.cn_multiple_paths, 'v1', DistanceType.SHORTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')
        self.assertEqual(result_1['v3'], 1, 'Shortest distance to v3 should be 1')

class TestInvalidInputs(unittest.TestCase):
    cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

    def test_invalid_distance_type(self):
        with self.assertRaises(Exception):
            single_source_dijkstra_vertices(TestInvalidInputs.cn, 'v1', 'INVALID_DISTANCE_TYPE', min_timing=0)

    def test_invalid_vertex(self):
        with self.assertRaises(simulation.model.EntityNotFound):
            single_source_dijkstra_vertices(TestInvalidInputs.cn, 'INVALID_VERTEX', DistanceType.SHORTEST, min_timing=0)

    @unittest.expectedFailure
    def test_invalid_min_timing(self):
        with self.assertRaises(Exception):
            single_source_dijkstra_vertices(TestInvalidInputs.cn, 'v1', DistanceType.SHORTEST, min_timing='INVALID_MIN_TIMING')