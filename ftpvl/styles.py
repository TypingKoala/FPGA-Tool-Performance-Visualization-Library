""" This module defines styles for ftpvl """
from typing import Callable
from ftpvl.evaluation import Evaluation
from ftpvl.processors import Processor

class Style(Processor):
    """
    Represents a type of processor that returns an evaluation containing CSS
    styles for visualization.
    """

    def process(self, input_eval: Evaluation) -> Evaluation:
        raise NotImplementedError

class ColorMapStyle(Style):
    """
    Represents a processor that uses a matplotlib colormap to style the input
    Evaluation.

    Values in the input are expected to be one of the following:
    * float between 0 and 1, inclusive
    * empty string

    Cells containing foats will be given a background color dependant on the
    color map, and empty strings will not be styled.
    """

    def __init__(self, cmap: Callable):
        self.cmap = cmap

    def process(self, input_eval: Evaluation) -> Evaluation:
        raise NotImplementedError
