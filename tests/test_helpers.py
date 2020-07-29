# pylint: disable=invalid-name

""" Tests for Helpers """
import unittest

import pandas as pd
from ftpvl.helpers import *


class TestHelpers():
    """
    Testing by partition:
        flatten(input_dict)
        get_versions(obj)
        rescale_actual_freq(freq)
        get_actual_freq(obj, hydra_clock_names)
        get_styling(val, cmap, val_range)
    """

    def test_flatten(self):
        """ Test if result is correctly flattened """
        result = flatten({"a": {"b": "c"}})
        assert result == {"a.b": "c"}

        result = flatten({"a": {"b": {"c": "d"}, "e": "f"}})
        assert result == {"a.b.c": "d", "a.e": "f"}

        result = flatten({"": {"": ""}})
        assert result == {".": ""}

        result = flatten({})
        assert result == {}

    def test_get_versions(self):
        """ Test if result correctly filters only keys that start with `version.` """
        result = get_versions({"versions.a": "10", "versions.b": "20", "c": "30"})
        assert result == {"versions.a": "10", "versions.b": "20"}

        result = get_versions({})
        assert result == {}

    def test_rescale_actual_freq(self):
        """ Test if rescaling works correctly """
        result = rescale_actual_freq(1_000_000)
        assert result == 1_000_000

        result = rescale_actual_freq(1_000_001)
        assert result == 1.000001

        result = rescale_actual_freq(1000)
        assert result == 1000

        result = rescale_actual_freq(32_000_000)
        assert result == 32

        result = rescale_actual_freq(5_000_000)
        assert result == 5

    def test_get_actual_freq(self):
        """ Test if get_actual_freq correctly extracts max frequency """
        obj = {
            "max_freq": 500
        }
        result = get_actual_freq(flatten(obj))
        assert result == 500

        obj = {
            "max_freq": {
                "clk": {
                    "actual": 12_000_000
                }
            }
        }
        result = get_actual_freq(flatten(obj))
        assert result == 12

    def test_get_actual_freq_hydra_clock_names(self):
        """ Test if get_actual_freq correctly selects the most important clock """

        # should select clk since it is higher priority
        obj = {
            "max_freq": {
                "clk": {
                    "actual": 12_000_000
                },
                "sys_clock": {
                    "actual": 24_000_000
                }
            }
        }
        result = get_actual_freq(flatten(obj), ["clk", "sys_clk", "clk_i"])
        assert result == 12

        # should select sys_clk since it is higher priority
        obj = {
            "max_freq": {
                "clk_i": {
                    "actual": 12_000_000
                },
                "sys_clk": {
                    "actual": 24_000_000
                }
            }
        }
        result = get_actual_freq(flatten(obj), ["clk", "sys_clk", "clk_i"])
        assert result == 24

        # should select clk_i since it is higher priority 
        obj = {
            "max_freq": {
                "clk_i": {
                    "actual": 12_000_000
                },
                "sys_clk": {
                    "actual": 24_000_000
                }
            }
        }
        result = get_actual_freq(flatten(obj), ["clk_i", "sys_clk", "clk"])
        assert result == 12

        # should select shortest clock name since none are specified
        obj = {
            "max_freq": {
                "cl": {
                    "actual": 12_000_000
                },
                "longer_cl": {
                    "actual": 24_000_000
                }
            }
        }
        result = get_actual_freq(flatten(obj), ["clk", "sys_clk", "clk_i"])
        assert result == 12
    
    def test_get_styling(self):
        """ Test if get_styling correctly queries colormap and returns correct
        CSS string """

        # specify mock colormap to improve test readability
        # mock checks if passed in val is expected
        def mock_colormap(expected_val):
            def colormap(val):
                assert val == expected_val, f"expected val to be {expected_val}, got {val}"
                return (1, 1, 1, 1)
            return colormap
        

        result = get_styling(0.5, mock_colormap(0.5))
        assert result == "background-color: #ffffff"

        result = get_styling(0, mock_colormap(0))
        assert result == "background-color: #ffffff"

        result = get_styling(5, mock_colormap(0.5), (0, 10))
        assert result == "background-color: #ffffff"

        result = get_styling(150, mock_colormap(0.5), (100, 200))
        assert result == "background-color: #ffffff"