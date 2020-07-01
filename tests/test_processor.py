""" Tests for Processors """

import pandas as pd
from pandas.testing import (
    assert_frame_equal, assert_series_equal, assert_index_equal
)

from ftpvl.processors import (
    AddNormalizedColumn,
    CleanDuplicates,
    MinusOne,
    StandardizeTypes,
    ExpandColumn,
    Reindex,
    SortIndex,
    NormalizeAround
)

from ftpvl.evaluation import Evaluation


class TestProcessor:
    """
    Testing by partition.

    MinusOne()
    StandardizeTypes()
    CleanDuplicates()
    AddNormalizedColumn()
    ExpandToolchain()
    Reindex()
    SortIndex()
    NormalizeAround()
    """

    def test_minusone(self):
        """ Test whether all values are correctly changed """

        df = pd.DataFrame({"a": [1, 2, 3, 4, 5]})
        eval1 = Evaluation(df)

        result = eval1.get_df()["a"]
        expected = pd.Series([1, 2, 3, 4, 5], name="a")

        assert_series_equal(result, expected)

        pipeline = [MinusOne()]
        result_processed = eval1.process(pipeline).get_df()["a"]
        expected_processed = pd.Series([0, 1, 2, 3, 4], name="a")

        assert_series_equal(result_processed, expected_processed)

    def test_standardizetypes(self):
        """ Test whether types are standardized """
        types = {"a": float}
        df = pd.DataFrame({"a": [1, 2, 3, 4, 5]})
        eval1 = Evaluation(df)

        assert eval1.get_df().dtypes["a"] == int

        pipeline = [StandardizeTypes(types)]

        result = eval1.process(pipeline)

        assert result.get_df().dtypes["a"] == float

    def test_cleanduplicates_no_duplicates(self):
        """ Test for evaluation that has no duplicates in specified column """
        df = pd.DataFrame(
            [
                {"a": 1, "b": 1, "c": 5},
                {"a": 1, "b": 2, "c": 4},
                {"a": 3, "b": 3, "c": 3},
                {"a": 4, "b": 4, "c": 2},
                {"a": 5, "b": 5, "c": 1},
            ]
        )
        eval1 = Evaluation(df)

        # test no duplicates
        pipeline = [CleanDuplicates(["b"])]
        result = eval1.process(pipeline).get_df()
        assert_frame_equal(result, df, check_like=True)

    def test_cleanduplicates_one_col(self):
        """ Test for evaluation that has duplicate in one column """
        df = pd.DataFrame(
            [
                {"a": 1, "b": 1, "c": 5},
                {"a": 1, "b": 2, "c": 4},
                {"a": 3, "b": 3, "c": 3},
                {"a": 4, "b": 4, "c": 2},
                {"a": 5, "b": 5, "c": 1},
            ]
        )
        eval1 = Evaluation(df)

        pipeline = [CleanDuplicates(["a"])]
        result = eval1.process(pipeline).get_df()
        expected = df.drop(1)

        assert_frame_equal(result, expected, check_like=True)

    def test_cleanduplicates_multi_col(self):
        """
        Test for evaluation that doesn't have duplicates when comparing
        more than one column
        """
        df = pd.DataFrame(
            [
                {"a": 1, "b": 1, "c": 5},
                {"a": 1, "b": 2, "c": 4},
                {"a": 3, "b": 3, "c": 3},
                {"a": 4, "b": 4, "c": 2},
                {"a": 5, "b": 5, "c": 1},
            ]
        )
        eval1 = Evaluation(df)
        pipeline = [CleanDuplicates(["a", "b"])]
        result2 = eval1.process(pipeline).get_df()
        assert_frame_equal(result2, df, check_like=True)

    def test_cleanduplicates_sorting(self):
        """
        Test by sorting before removing duplicate.
        """
        df = pd.DataFrame(
            [
                {"a": 1, "b": 1, "c": 5},
                {"a": 1, "b": 2, "c": 4},
                {"a": 3, "b": 3, "c": 3},
                {"a": 4, "b": 4, "c": 2},
                {"a": 5, "b": 5, "c": 1},
            ]
        )
        eval1 = Evaluation(df)

        pipeline = [CleanDuplicates(["a"], ["c"])]
        result = eval1.process(pipeline).get_df()  # will remove idx 1
        expected = df.drop(1)
        assert_frame_equal(result, expected, check_like=True)

        pipeline = [CleanDuplicates(["a"], ["c"], reverse_sort=True)]
        result = eval1.process(pipeline).get_df()  # will remove idx 0
        expected = df.drop(0).sort_index(level=0, ascending=False)
        assert_frame_equal(result, expected, check_like=True)

    def test_addnormalizedcolumn(self):
        """ Test whether normalized column is added """
        df = pd.DataFrame(
            [
                {"group": "a", "value": 10},
                {"group": "a", "value": 5},
                {"group": "a", "value": 3},
                {"group": "b", "value": 100},
                {"group": "b", "value": 31},
            ]
        )
        eval1 = Evaluation(df)

        pipeline = [AddNormalizedColumn("group", "value", "normalized")]
        result = eval1.process(pipeline).get_df()
        expected = pd.DataFrame(
            [
                {"group": "a", "value": 10, "normalized": 1.0},
                {"group": "a", "value": 5, "normalized": 0.5},
                {"group": "a", "value": 3, "normalized": 0.3},
                {"group": "b", "value": 100, "normalized": 1.0},
                {"group": "b", "value": 31, "normalized": 0.31},
            ]
        )

        assert_frame_equal(result, expected)

    def test_expandcolumn(self):
        """ Test whether the column is expanded """
        df = pd.DataFrame(
            [
                {"group": "a", "value": 10},
                {"group": "a", "value": 5},
                {"group": "a", "value": 3},
                {"group": "b", "value": 100},
                {"group": "b", "value": 31},
            ]
        )
        eval1 = Evaluation(df)

        mapping = {
            "a": ("a", "x"),
            "b": ("b", "y"),
        }

        pipeline = [ExpandColumn("group", ["group1", "group2"], mapping)]
        result = eval1.process(pipeline).get_df()
        expected = pd.DataFrame(
            [
                {"group": "a", "group1": "a", "group2": "x", "value": 10},
                {"group": "a", "group1": "a", "group2": "x", "value": 5},
                {"group": "a", "group1": "a", "group2": "x", "value": 3},
                {"group": "b", "group1": "b", "group2": "y", "value": 100},
                {"group": "b", "group1": "b", "group2": "y", "value": 31},
            ]
        )

        assert_frame_equal(result, expected, check_like=True)

    def test_reindex(self):
        """ Test whether the dataframe was reindexed """
        df = pd.DataFrame(
            [
                {"group": "a", "key": "a", "value": 10},
                {"group": "a", "key": "b", "value": 5},
                {"group": "a", "key": "c", "value": 3},
                {"group": "b", "key": "d", "value": 100},
                {"group": "b", "key": "e", "value": 31},
            ]
        )
        eval1 = Evaluation(df)

        pipeline = [Reindex(["value"])]
        result = eval1.process(pipeline).get_df()
        expected_index = pd.Index([10, 5, 3, 100, 31], name="value")
        assert_index_equal(result.index, expected_index)

        pipeline = [Reindex(["group", "key"])]
        result = eval1.process(pipeline).get_df()
        arrays = [["a", "a", "a", "b", "b"], ["a", "b", "c", "d", "e"]]
        expected_index = pd.MultiIndex.from_arrays(arrays, names=("group", "key"))
        assert_index_equal(result.index, expected_index)

    def test_sortindex(self):
        """ Test whether the dataframe is sorted by index """
        df = pd.DataFrame(
            data = [
                {"group": "a", "value": 10},
                {"group": "a", "value": 5},
                {"group": "a", "value": 3},
                {"group": "b", "value": 100},
                {"group": "b", "value": 31},
            ],
            index = pd.Index([
                5,
                4,
                3,
                2,
                1,
            ], name="idx")
        )
        
        eval1 = Evaluation(df)
        
        pipeline = [SortIndex(["idx"])]
        result = eval1.process(pipeline).get_df()
        expected = pd.DataFrame(
            data = [
                {"group": "b", "value": 31},
                {"group": "b", "value": 100},
                {"group": "a", "value": 3},
                {"group": "a", "value": 5},
                {"group": "a", "value": 10},
            ],
            index = pd.Index([
                1,
                2,
                3,
                4,
                5,
            ], name="idx")
        )
        assert_frame_equal(result, expected)


    def test_normalizearound(self):
        """
        Test whether all values are normalized around a certain (set of) rows
        """
        arrays = [
            ["blinky", "blinky", "blinky", "ibex", "ibex"],
            ["yosys", "yosys", "vivado", "yosys", "vivado"],
        ]
        index = pd.MultiIndex.from_arrays(arrays, names=("project", "synthesis_tool"))
        df = pd.DataFrame(
            data=[
                {"group": "b", "value": 0},
                {"group": "b", "value": 50},
                {"group": "b", "value": 100},
                {"group": "a", "value": 0},
                {"group": "a", "value": 10},
            ],
            index=index
        )
        eval1 = Evaluation(df)

        normalize_direction = {
            "value": 1
        }
        pipeline = [NormalizeAround(
            normalize_direction,
            group_by="project",
            idx_name="synthesis_tool",
            idx_value="vivado"
        )]

        result = eval1.process(pipeline).get_df()
        expected = pd.DataFrame(
            data=[
                {"group": "b", "value": 0},
                {"group": "b", "value": 0.25},
                {"group": "b", "value": 0.5},
                {"group": "a", "value": 0},
                {"group": "a", "value": 0.5},
            ],
            index=index
        )
        assert_frame_equal(result, expected)

    def test_normalizearound_negated(self):
        """
        Test whether all values are normalized in the correct direction based
        on the negation.
        """
        arrays = [
            ["blinky", "blinky", "blinky", "ibex", "ibex"],
            ["yosys", "yosys", "vivado", "yosys", "vivado"],
        ]
        index = pd.MultiIndex.from_arrays(arrays, names=("project", "synthesis_tool"))
        df = pd.DataFrame(
            data=[
                {"group": "b", "value": 0},
                {"group": "b", "value": 50},
                {"group": "b", "value": 100},
                {"group": "a", "value": 0},
                {"group": "a", "value": 10},
            ],
            index=index
        )
        eval1 = Evaluation(df)

        normalize_direction = {
            "value": -1
        }
        pipeline = [NormalizeAround(
            normalize_direction,
            group_by="project",
            idx_name="synthesis_tool",
            idx_value="vivado"
        )]

        result = eval1.process(pipeline).get_df()
        expected = pd.DataFrame(
            data=[
                {"group": "b", "value": 1},
                {"group": "b", "value": 0.75},
                {"group": "b", "value": 0.5},
                {"group": "a", "value": 1},
                {"group": "a", "value": 0.5},
            ],
            index=index
        )
        assert_frame_equal(result, expected)


