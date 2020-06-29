# pylint: disable=invalid-name

""" Tests for Evaluation class """
import unittest

import requests
import requests_mock

from ftpvl import HydraFetcher

class TestFetcher(unittest.TestCase):
    """
    Testing by partition.

    HydraFetcher:
        __init__(eval_num, mapping_dict)
        _download()
        _preprocess()
        get_evaluation()
    GCSFetcher:
        __init__(url, mapping_dict)
        _download()
        _preprocess()
        get_evaluation()
    """

    def test_hydrafetcher_init(self):
        """
        Calling init should save the arguments as an instance variable.
        """
        fetcher = HydraFetcher(eval_num=0, mapping={"a": "c", "b": "d"})

        self.assertEqual(fetcher.eval_num, 0)
        self.assertEqual(fetcher.mapping, {"a": "c", "b": "d"})

    @requests_mock.Mocker()
    def test_hydrafetcher_download(self, m):
        session = requests.Session()
        adapter = requests_mock.Adapter()
        session.mount('mock://', adapter)

    def test_hydrafetcher_preprocess(self):
        raise NotImplementedError

    def test_hydrafetcher_get_evaluation(self):
        raise NotImplementedError

    def test_hydrafetcher_integration(self):
        raise NotImplementedError
