""" This module defines processors for ftpvl. """

from ftpvl import Evaluation

class Processor():
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
            input: an Evaluation to process

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

    Attributes:
        types: a dictionary mapping metric names to a type (the type must be
            supported by Pandas)
    """

    def __init__(self, types: dict):
        """ Overrides Processor.__init__() """
        self.types = types

    def process(self, input_eval: Evaluation) -> Evaluation:
        raise NotImplementedError

# class CleanDuplicates(Processor):

# class AddRelativeFrequency(Processor):

# class ExpandToolchain(Processor):

# class Reindex(Processor):

# class SortIndex(Processor):

# class NormalizeAround(Processor):