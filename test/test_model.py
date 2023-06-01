from datetime import datetime
import unittest
from pathlib import Path
import json
import bz2
from simulation.model import CommunicationNetwork
import platform
from packaging import version



class ModelTest(unittest.TestCase):

    cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})
    cn1 = CommunicationNetwork({'h1': ['v1', 'v2', 'v3', 'v4', 'v5', 'v6'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

    def test_vertices(self):
        self.assertEqual(len(ModelTest.cn.vertices()), 4)
        self.assertEqual(ModelTest.cn.vertices(), {'v1', 'v2', 'v3', 'v4'})
        self.assertEqual(ModelTest.cn.vertices('h1'), {'v1', 'v2'})
        self.assertEqual(ModelTest.cn.vertices('h2'), {'v2', 'v3'})
        self.assertEqual(ModelTest.cn.vertices('h3'), {'v4', 'v3'})
        self.assertEqual(ModelTest.cn1.vertices('h1'), {'v1', 'v2', 'v3', 'v4', 'v5', 'v6'})

    def test_hyperedges(self):
        self.assertEqual(len(ModelTest.cn.hyperedges()), 3)
        self.assertEqual(ModelTest.cn.hyperedges('v1'), {'h1'})
        self.assertEqual(ModelTest.cn.hyperedges('v2'), {'h1', 'h2'})
        self.assertEqual(ModelTest.cn.hyperedges('v3'), {'h2', 'h3'})
        self.assertEqual(ModelTest.cn.hyperedges('v4'), {'h3'})

    def test_timings(self):
        self.assertEqual(len(ModelTest.cn.timings()), 3)
        self.assertEqual(ModelTest.cn.timings('h1'), 1)
        self.assertEqual(ModelTest.cn.timings('h2'), 2)
        self.assertEqual(ModelTest.cn.timings('h3'), 3)

    def test_empty_network(self):
        cn_empty = CommunicationNetwork({}, {})
        self.assertEqual(len(cn_empty.vertices()), 0)
        self.assertEqual(len(cn_empty.hyperedges()), 0)

    def test_isolated_vertex(self):
        cn_isolated = CommunicationNetwork({'h1': ['v1']}, {'h1': 1})
        self.assertEqual(len(cn_isolated.vertices()), 1)
        self.assertEqual(len(cn_isolated.hyperedges()), 1)

    def test_large_network(self):
            cn_very_large = CommunicationNetwork({f'h{i}': [f'v{j}' for j in range(1000)] for i in range(1000)}, {f'h{i}': i for i in range(1000)})
            self.assertEqual(len(cn_very_large.vertices()), 1000)
            self.assertEqual(len(cn_very_large.hyperedges()), 1000)

    # def test_correct_loading_of_json_data(self):
    #     test_file_path = Path('./data/networks/microsoft.json.bz2')  
    #     test_name = "test"

    #     test_data = {
    #     "1": {"participants": ["A", "B"], "end": "2023-05-26T11:08:38.766561"},
    #     }

    #     with open(test_file_path, 'w') as f:
    #         json.dump(test_data, f)

    #     instance = CommunicationNetwork.from_json(test_file_path, name=test_name)
        
    #     assert isinstance(instance, CommunicationNetwork)

    # def test_from_json_with_incorrect_bz2_data(self):
    #     test_file_path = "test.bz2"
        
    #     # Write some non-bz2 data to the file
    #     with open(test_file_path, 'wb') as f:
    #         f.write(b'not bz2 data')

    #     self.assertRaises(ValueError, CommunicationNetwork.from_json, test_file_path)

    # def test_from_json_with_non_bz2_compressed_file(self):
    #     test_file_path = Path('./data/networks/test.json.bz2')  # replace with your actual test file path

    #     # Write some non-bz2-compressed data to the file
    #     with open(test_file_path, 'wb') as f:
    #         f.write(b'some data')


    #     self.assertRaises(OSError, CommunicationNetwork.from_json, test_file_path)

class ModelDataTest(unittest.TestCase):
    def test_model_with_data(self):
        communciation_network = CommunicationNetwork.from_json('./data/networks/microsoft.json.bz2')
        self.assertEqual(len(communciation_network.participants()), 37103)
        self.assertEqual(len(communciation_network.channels()), 309740)

        self.assertEqual(len(communciation_network.vertices()), 37103)
        self.assertEqual(len(communciation_network.hyperedges()), 309740)


class TestJsonImport(unittest.TestCase):
    def test_json_module(self):
        try:
            import orjson
        except ImportError:
            orjson = None

        if 'orjson' in globals() and orjson is not None:
            json_module = orjson
        else:
            import json
            json_module = json

        if 'orjson' in globals():
            self.assertIs(json_module, orjson, "orjson module should be used when available")
        else:
            self.assertIs(json_module, json, "json module should be used when orjson is not available")
