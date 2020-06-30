# pylint: disable=invalid-name, line-too-long

""" Tests for Evaluation class """
import unittest
import json

import pandas as pd
import requests_mock

from pandas.testing import assert_frame_equal

from ftpvl import HydraFetcher


class TestHydraFetcherLarge(unittest.TestCase):
    """
    Testing by partition.

    HydraFetcher:
        __init__(eval_num, mapping_dict)
        get_evaluation()
            different eval_num
            different mapping
                exclusion, renaming
    """

    def test_hydrafetcher_init(self):
        """
        Calling init should save the arguments as an instance variable.
        """
        df_mappings = {
            "project": "project",
            "device": "device",
            "toolchain": "toolchain",
            "resources.BRAM": "bram",
            "resources.CARRY": "carry",
            "resources.DFF": "dff",
            "resources.IOB": "iob",
            "resources.LUT": "lut",
            "resources.PLL": "pll",
            "runtime.synthesis": "synthesis",
            "runtime.packing": "pack",
            "runtime.placement": "place",
            "runtime.routing": "route",
            "runtime.fasm": "fasm",
            "runtime.bitstream": "bitstream",
            "runtime.total": "total"
        }
        fetcher = HydraFetcher(eval_num=0, mapping=df_mappings)

        self.assertEqual(fetcher.eval_num, 0)
        self.assertEqual(fetcher.mapping, df_mappings)


    def test_hydrafetcher_get_evaluation(self):
        """
        get_evaluation() should return an Evaluation corresponding to the real
        dataset and mapping.
        """
        with requests_mock.Mocker() as m:
            evals_fn = 'tests/sample_data/evals.large.json'
            evals_url = 'https://hydra.vtr.tools/jobset/dusty/fpga-tool-perf/evals'

            meta_fn = 'tests/sample_data/meta.large.json'

            # setup /evals request mock
            evals_json_decoded = None
            with open(evals_fn, "r") as f:
                evals_json_encoded = f.read()
                evals_json_decoded = json.loads(evals_json_encoded)
                m.get(evals_url, text=evals_json_encoded)

            # setup /meta.json request mock
            with open(meta_fn, "r") as f:
                meta_json_encoded = f.read()
                for eval_obj in evals_json_decoded["evals"]:
                    for build_num in eval_obj["builds"]:
                        url = f'https://hydra.vtr.tools/build/{build_num}/download/1/meta.json'
                        m.get(url, text=meta_json_encoded)

            # run tests on different eval_num, up to 5
            for eval_num in range(len(evals_json_decoded["evals"])):
                with self.subTest(eval_num=eval_num):
                    print('subtest', eval_num)
                    # if mapping is not defined, should not remap
                    hf = HydraFetcher(eval_num=eval_num)
                    result = hf.get_evaluation().get_df()

                    expected_num_rows = len(evals_json_decoded['evals'][eval_num]['builds'])
                    self.assertEqual(len(result.index), expected_num_rows)

                    # TODO: more tests on real data


class TestGCSFetcherLarge(unittest.TestCase):
    """
    Testing by partition.

    GCSFetcher:
        __init__(url, mapping_dict)
        get_evaluation()
    """

    def test_gcsfetcher_init(self):
        raise NotImplementedError

    def test_gcsfetcher_get_evaluation(self):
        raise NotImplementedError
