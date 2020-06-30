# pylint: disable=invalid-name, line-too-long

""" Tests for Evaluation class """
import unittest

import pandas as pd
import requests_mock

from pandas.testing import assert_frame_equal, assert_series_equal

from ftpvl import HydraFetcher

class TestHydraFetcherSmall(unittest.TestCase):
    """
    Testing by partition.

    HydraFetcher:
        __init__(eval_num, mapping_dict, hydra_clock_names)
        get_evaluation()
            different eval_num
            different mapping
                exclusion, renaming
    """

    def test_hydrafetcher_init(self):
        """
        Calling init should save the arguments as an instance variable.
        """
        fetcher = HydraFetcher(
            eval_num=0,
            mapping={"a": "c", "b": "d"},
            hydra_clock_names=["clk", "clk1"]
        )

        self.assertEqual(fetcher.eval_num, 0)
        self.assertEqual(fetcher.mapping, {"a": "c", "b": "d"})
        self.assertEqual(fetcher.hydra_clock_names, ["clk", "clk1"])

    def test_hydrafetcher_get_evaluation_eval_num(self):
        """
        get_evaluation() should return an Evaluation corresponding to the small
        dataset and the specified eval_num.

        Tests different eval_num functionality.
        """
        with requests_mock.Mocker() as m:
            evals_fn = 'tests/sample_data/evals.small.json'
            evals_url = 'https://hydra.vtr.tools/jobset/dusty/fpga-tool-perf/evals'

            # load sample json data
            with open(evals_fn, "r") as f:
                json_data = f.read()
                m.get(evals_url, text=json_data) # setup /evals request mock

                for build_num in range(12):
                    url = f'https://hydra.vtr.tools/build/{build_num}/download/1/meta.json'
                    payload = {"build_num": build_num}
                    m.get(url, json=payload) # setup /meta.json request mock

            # run tests on different eval_num
            for eval_num in range(0, 3):
                with self.subTest(eval_num=eval_num):
                    # if mapping is not defined, should not remap
                    hf = HydraFetcher(eval_num=eval_num)
                    result = hf.get_evaluation().get_df()

                    col = [x for x in range(eval_num * 4, eval_num * 4 + 4)]
                    expected = pd.DataFrame({"build_num": col})
                    assert_frame_equal(result, expected)

    def test_hydrafetcher_get_evaluation_mapping(self):
        """
        get_evaluation() should return an Evaluation corresponding to the small
        dataset and mapping.

        Tests whether exclusion and renaming works when remapping.
        """
        with requests_mock.Mocker() as m:
            evals_fn = 'tests/sample_data/evals.small.json'
            evals_url = 'https://hydra.vtr.tools/jobset/dusty/fpga-tool-perf/evals'

            # load sample json data
            with open(evals_fn, "r") as f:
                json_data = f.read()
                m.get(evals_url, text=json_data) # setup /evals request mock

                for build_num in range(4):
                    url = f'https://hydra.vtr.tools/build/{build_num}/download/1/meta.json'
                    payload = {"build_num": build_num, "extra": 1}
                    m.get(url, json=payload) # setup /meta.json request mock

            # test exclusion
            hf1 = HydraFetcher(eval_num=0,
                               mapping={"build_num": "build_num"})
            result1 = hf1.get_evaluation().get_df()

            col = [x for x in range(4)]
            expected1 = pd.DataFrame({"build_num": col})

            assert_frame_equal(result1, expected1)

            # test renaming
            hf2 = HydraFetcher(eval_num=0,
                               mapping={"build_num": "renamed_num"})
            result2 = hf2.get_evaluation().get_df()

            col = [x for x in range(4)]
            expected2 = pd.DataFrame({"renamed_num": col})

            assert_frame_equal(result2, expected2)

    def test_hydrafetcher_hydra_clock_names(self):
        """
        get_evaluation() should return an Evaluation corresponding to the small
        dataset and hydra_clock_names attribute.

        Tests whether the ordering of hydra_clock_names is correctly 
        implemented.
        """
        with requests_mock.Mocker() as m:
            evals_fn = 'tests/sample_data/evals.small.json'
            evals_url = 'https://hydra.vtr.tools/jobset/dusty/fpga-tool-perf/evals'

            # load sample json data
            with open(evals_fn, "r") as f:
                json_data = f.read()
                m.get(evals_url, text=json_data) # setup /evals request mock

                for build_num in range(4):
                    url = f'https://hydra.vtr.tools/build/{build_num}/download/1/meta.json'
                    payload = {
                        "max_freq": {
                            "clk": {
                                "actual": 100
                            },
                            "clk_i": {
                                "actual": 200
                            },
                            "sys_clk": {
                                "actual": 300
                            }
                        }
                    }
                    m.get(url, json=payload) # setup /meta.json request mock

            # test which clock is chosen if there are multiple clocks

            # format test cases as tuples:
            # ({hydra_clock_names}, {expected_clock})
            test_cases = [
                (["clk", "clk_i", "sys_clk"], 100),
                (["clk_i", "sys_clk", "clk"], 200),
                (["sys_clk", "clk", "clk_i"], 300),
            ]

            for hydra_clock_name, expected_clock in test_cases:
                with self.subTest(hydra_clock_name=hydra_clock_name):
                    hf = HydraFetcher(eval_num=0, hydra_clock_names=hydra_clock_name)
                    result = hf.get_evaluation().get_df()

                    expected_col = [expected_clock for _ in range(4)]
                    expected_series = pd.Series(expected_col, name="freq")
                    assert_series_equal(result["freq"], expected_series)
            
            # test that the shortest clock name is chosen if no matches
            hf = HydraFetcher(eval_num=0, hydra_clock_names=[])
            result = hf.get_evaluation().get_df()

            expected_col = [100 for _ in range(4)]
            expected_series = pd.Series(expected_col, name="freq")
            assert_series_equal(result["freq"], expected_series)


class TestJSONFetcherSmall(unittest.TestCase):
    """
    Testing by partition.

    JSONFetcher:
        __init__(path, mapping_dict)
        get_evaluation()
    """

    def test_gcsfetcher_init(self):
        raise NotImplementedError

    def test_gcsfetcher_get_evaluation_eval_num(self):
        raise NotImplementedError

    def test_gcsfetcher_get_evaluation_mapping(self):
        raise NotImplementedError
