# pylint: disable=invalid-name, line-too-long

""" Tests for Evaluation class """
import unittest
import json

import pandas as pd
import requests_mock

from pandas.testing import assert_series_equal

from ftpvl.fetchers import HydraFetcher, JSONFetcher


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
        fetcher = HydraFetcher(
            project="dusty",
            jobset="fpga-tool-perf",
            eval_num=0,
            mapping=df_mappings)

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

            # run tests on different eval_num
            for eval_num in range(len(evals_json_decoded["evals"])):
                with self.subTest(eval_num=eval_num):
                    # if mapping is not defined, should not remap
                    if len(evals_json_decoded["evals"][eval_num]["builds"]) == 0:
                        continue # otherwise hydrafetcher will throw error
                    hf = HydraFetcher(
                        project="dusty",
                        jobset="fpga-tool-perf",
                        eval_num=eval_num)
                    result = hf.get_evaluation().get_df()

                    expected_num_rows = len(evals_json_decoded['evals'][eval_num]['builds'])
                    self.assertEqual(len(result.index), expected_num_rows)

                    # TODO: more tests on real data


class TestJSONFetcherLarge(unittest.TestCase):
    """
    Testing by partition.

    JSONFetcher:
        __init__(path, mapping_dict)
        get_evaluation()
    """

    def test_jsonfetcher_init(self):
        """
        Calling init should save the arguments as an instance variable.
        """
        df_mappings = {
            "project": "project",
            "device": "device",
            "toolchain": "toolchain",
            "clock_actual_frequency": "freq",
            "#BRAM": "bram",
            "#CARRY": "carry",
            "#DFF": "dff",
            "#IOB": "iob",
            "#LUT": "lut",
            "#PLL": "pll",
            "synthesis_time": "synthesis",
            "packing_time": "pack",
            "placement_time": "place",
            "routing_time": "route",
            "fasm_time": "fasm",
            "bitstream_time": "bitstream",
            "total_time": "total"
        }

        path = 'tests/sample_data/dataframe.json'
        fetcher = JSONFetcher(path, df_mappings)

        assert fetcher.path == path
        assert fetcher.mapping == df_mappings

    def test_jsonfetcher_get_evaluation(self):
        """
        get_evaluation() should return an Evaluation corresponding to the small
        dataset.
        """
        fetcher = JSONFetcher('tests/sample_data/dataframe.json')
        result = fetcher.get_evaluation().get_df()

        expected_projects = pd.Series(
            ['ibex',
             'oneblink',
             'litex-linux',
             'oneblink',
             'litex-linux',
             'picosoc-spimemio-wrap',
             'oneblink',
             'picosoc-simpleuart-wrap',
             'picosoc-simpleuart-wrap',
             'murax',
             'oneblink',
             'blinky',
             'vexriscv-verilog',
             'picosoc-spimemio-wrap',
             'hamsternz-hdmi',
             'picosoc-wrap',
             'blinky',
             'oneblink',
             'vexriscv-smp',
             'blinky',
             'oneblink',
             'picosoc-wrap',
             'vexriscv-verilog',
             'picosoc-wrap',
             'vexriscv-verilog',
             'picosoc-simpleuart-wrap',
             'oneblink',
             'vexriscv-verilog',
             'blinky',
             'blinky',
             'picorv32-wrap',
             'litex-linux',
             'litex-linux',
             'picorv32-wrap',
             'oneblink',
             'oneblink',
             'picosoc-spimemio-wrap',
             'murax',
             'picorv32-wrap',
             'oneblink',
             'ibex',
             'murax',
             'picorv32-wrap',
             'blinky',
             'oneblink',
             'picorv32-wrap',
             'picorv32-wrap',
             'oneblink',
             'oneblink'],
            name="project"
        )
        assert_series_equal(result["project"], expected_projects)
