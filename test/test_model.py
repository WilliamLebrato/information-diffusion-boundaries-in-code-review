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

    def test_vertices(self):
        self.assertEqual(len(ModelTest.cn.vertices()), 4)
        self.assertEqual(ModelTest.cn.vertices('h1'), {'v1', 'v2'})

    def test_hyperedges(self):
        self.assertEqual(len(ModelTest.cn.hyperedges()), 3)
        self.assertEqual(ModelTest.cn.hyperedges('v1'), {'h1'})

    def test_timings(self):
        self.assertEqual(len(ModelTest.cn.timings()), 3)
        self.assertEqual(ModelTest.cn.timings('h1'), 1)
        self.assertEqual(ModelTest.cn.timings('h2'), 2)
        self.assertEqual(ModelTest.cn.timings('h3'), 3)

    def test_empty_network(self):
        cn_empty = CommunicationNetwork({}, {})
        self.assertEqual(len(cn_empty.vertices()), 0)
        self.assertEqual(len(cn_empty.hyperedges()), 0)

    
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
