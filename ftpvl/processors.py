""" Processors transform Evaluations to be more useful when visualized. """
import math
from typing import Any, Callable, Dict, List, Union

import numpy as np
import pandas as pd
from ftpvl.evaluation import Evaluation
from scipy import stats


class Processor:
    """
    Superclass for all processors that can be applied to Evaluation instances.

    All processors have a method process() that take an Evaluation instance and
    returns an Evaluation that has been processed in some way. The behavior of
    this method is specified by the specific subclass and its parameters.
    """

    def process(self, input_eval: Evaluation) -> Evaluation:
        raise NotImplementedError


class MinusOne(Processor):
    """
    Processor that returns the input Evaluation by subtracting one from every
    data value.

    This processor is useful for testing the functionality of processors on
    Evaluations.
    """

    def process(self, input_eval: Evaluation) -> Evaluation:
        return Evaluation(input_eval.get_df() - 1, input_eval.get_eval_id())


class StandardizeTypes(Processor):
    """
    Processor that casts metrics in an Evaluation to the specified type.

    The type of each metric in an Evaluation is inferred after
    fetching. This processor accepts a dictionary of types and casts the
    Evaluation to those types.

    Parameters
    ----------
    types : dict
        A mapping from column names to types
    """

    def __init__(self, types: dict):
        self.types = types

    def process(self, input_eval: Evaluation) -> Evaluation:
        input_df = input_eval.get_df()

        try:
            # if int, we might need to convert to float first
            # (e.g. int(float("6.0")))
            if int in self.types.values():
                # create dictionary replacing int with float
                pre_df_types = {
                    k: (v if v != int else float) for k, v in self.types.items()
                }
                input_df = input_df.astype(pre_df_types)

            new_df = input_df.astype(self.types)
        except KeyError:
            raise KeyError("A key in the types parameter does not exist in the evaluation.")
        return Evaluation(new_df, input_eval.get_eval_id())


class CleanDuplicates(Processor):
    """
    Processor that outputs a new dataframe that removes duplicate rows.
    Optionally can sort the dataframe before removing duplicates.

    Two rows are considered duplicates if and only if all values specified in 
    duplicate_col_names matches.

    By default, the first instance of a duplicate is retained, and all others
    are removed. You can optionally specify columns to sort by and which way to
    sort, which provides fine-grained control over which rows are removed.

    Parameters
    ----------
    duplicate_col_names : List[str]
        column names to use when finding duplicates

    sort_col_names : List[str], optional
        column names to sort by, by default None
 
    reverse_sort : bool, optional
        sort in ascending order, by default False
    """

    def __init__(
        self,
        duplicate_col_names: List[str],
        sort_col_names: List[str] = None,
        reverse_sort: bool = False,
    ):

        self._duplicate_col_names = duplicate_col_names
        self._sort_col_names = sort_col_names
        self._reverse_sort = reverse_sort

    def process(self, input_eval: Evaluation) -> Evaluation:
        if self._sort_col_names is None:
            new_df = input_eval.get_df().drop_duplicates(
                subset=self._duplicate_col_names
            )
            return Evaluation(new_df, input_eval.get_eval_id())
        else:
            new_df = (
                input_eval.get_df()
                .sort_values(by=self._sort_col_names, ascending=self._reverse_sort)
                .drop_duplicates(subset=self._duplicate_col_names)
            )
            return Evaluation(new_df, input_eval.get_eval_id())


class AddNormalizedColumn(Processor):
    """
    Processor that groups rows by a column, finds the best value of the
    specified column, and adds a new column with the normalized values of the
    row compared to the best value.

    The best value is specified by the direction parameter. If the direction
    is `1`, then the best value is the maximum. If direction is `-1`, then the
    best value is the minimum.

    Parameters
    ----------
    groupby : str
        the column to group by
    
    input_col_name : str
        the input column to normalize

    output_col_name : str
        the column to write the normalized values to

    direction : int (either 1 or -1)
        the direction to find the best value to normalize against. If 1, then
        the best value is the max and all other values are compared to it. If -1,
        the best value is the min and all other values are compared to it.
    """

    def __init__(self, groupby: str, input_col_name: str, output_col_name: str, direction: int = 1):

        self._groupby = groupby
        self._input_col_name = input_col_name
        self._output_col_name = output_col_name
        
        assert direction in [1, -1], "direction must be either 1 or -1"
        self._direction = direction

    def _normalize(self, input_df: pd.DataFrame):
        """
        Given a dataframe, find the max value of the input col name and
        create a new column with the normalized value of each row
        """
        if self._direction == 1:
            max_val = input_df[self._input_col_name].max()
        else:
            max_val = input_df[self._input_col_name].min()
        input_df[self._output_col_name] = input_df[self._input_col_name] / max_val
        return input_df

    def process(self, input_eval: Evaluation) -> Evaluation:
        input_df = input_eval.get_df()
        new_df = input_df.groupby(self._groupby).apply(self._normalize)

        return Evaluation(new_df, input_eval.get_eval_id())


class ExpandColumn(Processor):
    """
    Processor that turns one column into more than one column by mapping values
    of a column to multiple values.

    Parameters
    ----------
    input_col_name : str
        the column name to map from

    output_col_names : List[str]
        the column names to map to

    mapping : Dict[str, List[str]]
        a dictionary mapping a value to a list of values. The processor will
        look at the value at input_col_name, use it as the key to index into mapping, and 
        get the corresponding list of strings that will used as the values for the new 
        metrics with names in output_col_names.
    """

    def __init__(self, input_col_name: str, output_col_names: List[str], mapping: Dict[str, List[str]]):

        self._input_col_name = input_col_name
        self._output_col_names = output_col_names
        self._mapping = mapping

    def _expansion(self, input_df: pd.DataFrame):
        """
        Given a dataframe that contains only one unique value in
        _input_col_name, writes new columns as defined by _output_col_names and
        _mapping and returns the new dataframe
        """
        group_value = input_df[self._input_col_name].iloc[0]

        # check for invalid input
        assert group_value in self._mapping.keys(), f"{group_value} not in mapping"
        assert len(self._output_col_names) == len(
            self._mapping[group_value]
        ), f"{group_value} mapping length does not equal output_col_name length"

        for output_idx in range(len(self._output_col_names)):
            input_df[self._output_col_names[output_idx]] = self._mapping[group_value][
                output_idx
            ]

        return input_df

    def process(self, input_eval: Evaluation) -> Evaluation:
        input_df = input_eval.get_df()
        new_df = input_df.groupby(self._input_col_name).apply(self._expansion)

        return Evaluation(new_df, input_eval.get_eval_id())


class Reindex(Processor):
    """
    Processor that reassigns current columns as indices for improved
    visualization.

    Reindexing is useful for grouping similar results in the final
    visualization, since each row is identified by a (usually-unique)
    value in the index. Indices are always the first columns, which
    improves readability of the final visualization.

    Parameters
    ----------
    reindex_names : List[str]
        A list of column names to reindex
    """

    def __init__(self, reindex_names: List[str]):
        self._reindex_names = reindex_names

    def process(self, input_eval: Evaluation) -> Evaluation:
        input_df = input_eval.get_df()
        new_df = input_df.set_index(self._reindex_names)
        return Evaluation(new_df, input_eval.get_eval_id())


class SortIndex(Processor):
    """
    Processor that sorts an evaluation by indices.

    Parameters
    ----------
    sort_names : List[str]
        a list of index names to sort by
    """

    def __init__(self, sort_names: List[str]):
        self._sort_names = sort_names

    def process(self, input_eval: Evaluation) -> Evaluation:
        input_df = input_eval.get_df()
        new_df = input_df.sort_index(level=self._sort_names)
        return Evaluation(new_df, input_eval.get_eval_id())


class NormalizeAround(Processor):
    """
    Processor that normalizes all specified values in an Evaluation around
    a baseline that is chosen based on a specified index name and value.

    All normalized values are between 0 and 1, with 0.5 being the baseline.
    This is useful in creating styles that show relative differences between
    each row and the baseline.

    Parameters
    ----------
    normalize_direction : dict
        a dictionary mapping column names to 1 or -1. If a value is
        optimized when smaller, set the negation to 1. If it is optimized
        when larger, set the negation to -1. If there is no entry,
        normalization is skipped.

    group_by : str
        the column name used to group results before finding the baseline
        of the group and normalizing

    idx_name : str
        the name of the index used to find the baseline result. The baseline
        result will become the baseline which all other grouped results will be
        normalized by

    idx_value : str
        the value of the baseline result at idx_name
    """

    def __init__(self, normalize_direction: dict, group_by: str, idx_name: str, idx_value: str):
        self._groupby = group_by
        self._idx_name = idx_name
        self._idx_value = idx_value

        self._column_names = []
        self._column_negations = []
        for name, negation in normalize_direction.items():
            self._column_names.append(name)
            self._column_negations.append(negation)

    def _normalize_around(self, input_df):
        """
        Given a dataframe, finds the baseline using the specified index name
        and value, and normalizes all other rows around it. Only affects items
        specified in normalize_direction. Returns the altered df.
        """
        is_baseline = input_df.index.get_level_values(self._idx_name) == self._idx_value

        # get stats for baseline
        base = input_df.loc[is_baseline, self._column_names].iloc[0]
        scaling_factor = (input_df[self._column_names] - base).abs().max()

        # rescale values to between -1 and 1
        scaled = (input_df[self._column_names] - base) / scaling_factor
        scaled *= self._column_negations

        # rescale values to between 0 and 1
        offset = (scaled / 2) + 0.5
        input_df[self._column_names] = offset
        return input_df

    def process(self, input_eval: Evaluation) -> Evaluation:
        input_df = input_eval.get_df()
        new_df = input_df.groupby(self._groupby).apply(self._normalize_around)
        return Evaluation(new_df, input_eval.get_eval_id())


class Normalize(Processor):
    """
    Processor that normalizes all specified values in an Evaluation by column
    around zero.

    All normalized values are between 0 and 1, with 0.5 being the baseline.
    Therefore, a value of zero is mapped to 0.5, positive values are mapped
    to values > 0.5, and negative values are mapped to values < 0.5.

    This is useful in creating styles for evaluations that have already
    performed calculations to compare multiple evaluations. For example, you
    can subtract one evaluation from another, then apply this processor before
    styling.

    Parameters
    ----------
    normalize_direction : dict
        a dictionary mapping column names to 1 or -1. If a value is optimized
        when smaller, set the negation to 1. If it is optimized when larger, set
        the negation to -1. If there is no entry, normalization is skipped.
    """

    def __init__(self, normalize_direction: dict):

        self._column_names = []
        self._column_negations = []
        for name, negation in normalize_direction.items():
            self._column_names.append(name)
            self._column_negations.append(negation)

    def _normalize(self, input_df):
        """
        Given a dataframe, normalizes each column. Only affects items
        specified in normalize_direction. Returns the altered df.
        """

        # find scaling factor
        scaling_factor = (input_df[self._column_names]).abs().max()

        # rescale values to between -1 and 1
        scaled = (input_df[self._column_names]) / scaling_factor
        scaled *= self._column_negations

        # rescale values to between 0 and 1
        offset = (scaled / 2) + 0.5
        input_df[self._column_names] = offset
        return input_df

    def process(self, input_eval: Evaluation) -> Evaluation:
        input_df = input_eval.get_df()
        new_df = self._normalize(input_df)
        return Evaluation(new_df, input_eval.get_eval_id())

class RelativeDiff(Processor):
    """
    Processor that outputs the relative difference between evaluation A and B.

    All numeric metrics will be compared, and all others will not be included in
    the output. B is compared to A, where the output is greater than 0 if B is
    greater than A, and less than 0 otherwise.

    The calculation performed is (B - A) / A, where B is the evaluation that
    this processor is being applied to and A is the evaluation passed as a
    parameter.

    Parameters
    ----------
    a : Evaluation
        The evaluation to use when comparing against the Evaluation that is
        being processed. Corresponds to evaluation A in the description.

    Examples
    --------
    >>> a = Evaluation(pd.DataFrame(
    ... data=[
    ...     {"x": 1, "y": 5},
    ...     {"x": 4, "y": 10}
    ... ]))
    >>> b = Evaluation(pd.DataFrame(
    ... data=[
    ...     {"x": 2, "y": 20},
    ...     {"x": 2, "y": 2}
    ... ]))
    >>> b.process([RelativeDiff(a)]).get_df()
         x    y
    0  1.0  3.0
    1 -0.5 -0.8
    """

    def __init__(self, a: Evaluation):
        self.a = a

    def process(self, b: Evaluation) -> Evaluation:
        a_nums = self.a.get_df().select_dtypes(include=[np.number])
        b_nums = b.get_df().select_dtypes(include=[np.number])
        diff = (b_nums - a_nums) / a_nums
        difference_eval = Evaluation(diff)

        return difference_eval

class FilterByIndex(Processor):
    """
    Processor that filters an Evaluation by matching a specified index value
    after indexing.

    This is best used in a processing pipeline after the Reindex processor.
    For filtering an evaluation based on metrics (which is not an index),
    use the FilterByMetric processor.

    Parameters
    ----------
    index_name : str
        the name of the index to use when filtering
    index_value : Any
        the value to compare with
    
    Examples
    --------
    >>> a = Evaluation(pd.DataFrame(
    ... data=[
    ...     {"x": 1, "y": 5},
    ...     {"x": 4, "y": 10}
    ... ],
    ... index=pd.Index(["a", "b"], name="key")))
    >>> a.process([FilterByIndex("key", "a")]).get_df()
        x    y
    key
    a   1    5
    """
    def __init__(self, index_name: str, index_value: Any):
        self.index_name = index_name
        self.index_value = index_value
    
    def process(self, input_eval: Evaluation):
        old_df = input_eval.get_df()
        if isinstance(old_df.index, pd.MultiIndex):
            new_df = old_df.xs(self.index_value, level=self.index_name)
        elif isinstance(old_df.index, pd.Index):
            # slicing instead of indexing to maintain shape
            new_df = old_df.loc[self.index_value:self.index_value]
        else:
            raise ValueError("Incompatible dataframe index.")
        return Evaluation(new_df, input_eval.get_eval_id())

class Aggregate(Processor):
    """
    Processor that allows you to aggregate all the numeric fields of an
    Evaluation using a specified function.

    This acts as a superclass for specific aggregator implementations, such as
    GeomeanAggregate. It can also be used for custom aggregations, by supplying
    an aggregator function to the constructor.

    Parameters
    ----------
    func : Callable[[pd.Series], Union[int, float]]
        a function that takes a Pandas Series and aggregates it into a single
        number, possibly a NaN value

    Examples
    --------
    >>> a = Evaluation(pd.DataFrame(
    ... data=[
    ...     {"x": 1, "y": 5},
    ...     {"x": 4, "y": 10}
    ... ]))
    >>> a.process([Aggregate(lambda x: x.sum())]).get_df()
        x    y
    0   5    15
    """
    def __init__(self, func: Callable[[pd.Series], Union[int, float]]):
        self.func = func
    
    def process(self, input_eval: Evaluation):
        old_df = input_eval.get_df()
        numeric_columns = old_df.select_dtypes(include=['number']).dropna(axis=1).columns
        new_df = pd.DataFrame([old_df[numeric_columns].agg(self.func)])
        return Evaluation(new_df, input_eval.get_eval_id())

class GeomeanAggregate(Aggregate):
    """
    Processor that aggregates an entire Evaluation by finding the geometric mean of each
    numeric metric.

    Subclass of Aggregate class.

    Examples
    --------
    >>> a = Evaluation(pd.DataFrame(
    ... data=[
    ...     {"x": 1, "y": 8},
    ...     {"x": 4, "y": 8}
    ... ]))
    >>> a.process([GeomeanAggregate()).get_df()
        x    y
    0   2    8
    """
    def __init__(self):
        def geomean(x):
            x = x.dropna()
            return stats.gmean(x) if not x.empty else math.nan
        super().__init__(geomean)
