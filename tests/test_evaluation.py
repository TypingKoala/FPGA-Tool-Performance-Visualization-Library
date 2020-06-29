# pylint: disable=invalid-name

""" Tests for Evaluation class """
import unittest

import pandas as pd
from ftpvl import Evaluation, MinusOne

class TestEvaluation(unittest.TestCase):
    """
    Testing by partition:
        __init__()
        get_df()
            defensive copying
        process(List[Processor])
            0, 1, 1+ processors
    """

    def test_evaluation_get_df_equality(self):
        """
        get_df() should return a dataframe with values equal to constructor
        argument
        """
        df = pd.DataFrame([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
        result = Evaluation(df).get_df()

        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.equals(df))

    def test_evaluation_get_df_defensive_copy(self):
        """
        get_df() should return a copy of the constructor argument to prevent
        caller from mutating the dataframe
        """
        df = pd.DataFrame([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
        result = Evaluation(df).get_df()

        result["a"][0] = 5 # mutate result

        self.assertFalse(result.equals(df))

    def test_evaluation_process_empty(self):
        """
        Calling process() with an empty list of processors should return the
        input DF without any changes.
        """
        df = pd.DataFrame([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
        result = Evaluation(df).process([]).get_df()

        self.assertTrue(result.equals(df))

    def test_evaluation_process_single(self):
        """
        Calling process() with one MinusOne should return a new df that
        subtract one from every input value, but not affect the input dataframe.
        """
        pipeline = [MinusOne()]

        df = pd.DataFrame([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
        result = Evaluation(df).process(pipeline).get_df()
        expected = pd.DataFrame([{"a": 0, "b": 1}, {"a": 2, "b": 3}])

        # check if input eval has been altered
        self.assertFalse(result.equals(df))
        self.assertFalse(df.equals(expected))

        # check if output eval has correct values
        self.assertTrue(result.equals(expected))


    def test_evaluation_process_multiple(self):
        """
        Calling process() with two MinusOne should return a new df that
        subtract two from every input value, but not affect the input dataframe.
        """
        pipeline = [MinusOne(), MinusOne()]

        df = pd.DataFrame([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
        result = Evaluation(df).process(pipeline).get_df()
        expected = pd.DataFrame([{"a": -1, "b": 0}, {"a": 1, "b": 2}])

        # check if input eval has been altered
        self.assertFalse(result.equals(df))
        self.assertFalse(df.equals(expected))

        # check if output eval has correct values
        self.assertTrue(result.equals(expected))
