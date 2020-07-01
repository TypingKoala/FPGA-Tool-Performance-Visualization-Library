""" This module defines processors for ftpvl. """

from typing import List
from ftpvl import Evaluation


class Processor:
    """
    Superclass for all processors that can be applied to Evaluation instances.

    All processors have a method process() that take an Evaluation instance and
    returns an Evaluation that has been processed in some way. The behavior of
    this method is specified by the specific subclass and its parameters.
    """

    def process(self, input_eval: Evaluation) -> Evaluation:
        """
        Given an Evaluation instance, returns a new Evaluation instance that
        is processed.

        This method does not mutate the input Evaluation.

        Args:
            input_eval: an Evaluation to process

        Returns:
            a processed Evaluation object
        """
        raise NotImplementedError


class MinusOne(Processor):
    """
    Processor that returns the input Evaluation by subtracting one from every
    data value.

    This processor is useful for testing the functionality of processors on
    Evaluations.
    """

    def process(self, input_eval: Evaluation) -> Evaluation:
        return Evaluation(input_eval.get_df() - 1)


class StandardizeTypes(Processor):
    """
    Processor that casts metrics in an Evaluation to the specified type.

    The type of each metric in an Evaluation is inferred after
    fetching. This processor accepts a dictionary of types and casts the
    Evaluation to those types.
    """

    def __init__(self, types: dict):
        """Initializes StandardizeTypes processor.

        Args:
            types (dict): A dictionary mapping column names to types.
        """
        self._types = types

    def process(self, input_eval: Evaluation) -> Evaluation:
        df = input_eval.get_df()

        # if int, we might need to convert to float first
        # (e.g. int(float("6.0")))
        if int in self._types.values():
            # create dictionary replacing int with float
            pre_df_types = {
                k: (v if v != int else float) for k, v in self._types.items()
            }
            df = df.astype(pre_df_types)

        new_df = df.astype(self._types)
        return Evaluation(new_df)


class CleanDuplicates(Processor):
    """
    Processor that removes duplicate rows from an Evaluation dataframe based on
    one or more values in each row.

    By default, the first instance of a duplicate is retained, and all others
    are removed. You can optionally specify columns to sort by and which way to
    sort, which provides fine-grained control over which rows are removed.
    """

    def __init__(
        self,
        duplicate_col_names: List[str],
        sort_col_names: List[str] = None,
        reverse_sort: bool = False,
    ):
        """Initializes CleanDuplicates processor.

        Args:
            duplicate_col_names (List[str]): column names to use when finding
                duplicates
            sort_col_names (List[str], optional): column names to sort by.
                Defaults to None.
            reverse_sort (bool, optional): If True, sorts in ascending order.
                Defaults to False.
        """
        self._duplicate_col_names = duplicate_col_names
        self._sort_col_names = sort_col_names
        self._reverse_sort = reverse_sort

    def process(self, input_eval: Evaluation) -> Evaluation:
        if self._sort_col_names is None:
            new_df = input_eval.get_df().drop_duplicates(
                subset=self._duplicate_col_names
            )
            return Evaluation(new_df)
        else:
            new_df = (
                input_eval.get_df()
                .sort_values(by=self._sort_col_names, ascending=self._reverse_sort)
                .drop_duplicates(subset=self._duplicate_col_names)
            )
            return Evaluation(new_df)

class AddNormalizedColumn(Processor):
    """
    Processor that groups rows by a column, calculates the maximum of the
    specified column, and adds a new column with the normalized values of the
    row compared to the max.
    """
    def __init__(self, groupby: str, input_col_name: str, output_col_name: str):
        """Initializes the AddNormalizedColumn processor.

        Args:
            groupby (str): the column to group by
            input_col_name (str): the input column to normalize
            output_col_name (str): the column to write the normalized values to
        """
        self._groupby = groupby
        self._input_col_name = input_col_name
        self._output_col_name = output_col_name

    def _normalize(self, df):
        """
        Given a dataframe, find the max value of the input col name and
        create a new column with the normalized value of each row
        """
        max_val = df[self._input_col_name].max()
        df[self._output_col_name] = df[self._input_col_name] / max_val
        return df

    def process(self, input_eval: Evaluation) -> Evaluation:
        df = input_eval.get_df()
        new_df = df.groupby(self._groupby).apply(self._normalize)

        return Evaluation(new_df)


# class ExpandToolchain(Processor):
#     raise NotImplementedError


# class Reindex(Processor):
#     raise NotImplementedError


# class SortIndex(Processor):
#     raise NotImplementedError


# class NormalizeAround(Processor):
#     raise NotImplementedError
