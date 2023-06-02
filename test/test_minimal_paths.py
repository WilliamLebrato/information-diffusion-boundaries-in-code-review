import unittest
import simulation.model

from simulation.model import CommunicationNetwork
from simulation.minimal_paths import single_source_dijkstra_vertices, single_source_dijkstra_hyperedges, DistanceType



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

    
    def test_single_vertex(self): # (FAILS)
        self.assertEqual(single_source_dijkstra_vertices(TestBoundaryCases.cn_single_vertex, 'v1', DistanceType.SHORTEST, min_timing=0), {'v1': 0}, 'Provided a graph of only one vertex the expected result is a dictionary with one key and the value 0.')
        self.assertEqual(single_source_dijkstra_hyperedges(TestBoundaryCases.cn_single_vertex, 'v1', DistanceType.SHORTEST, min_timing=0), {'v1': 0}, 'Provided a graph of only one vertex the expected result is a dictionary with one key and the value 0.')

