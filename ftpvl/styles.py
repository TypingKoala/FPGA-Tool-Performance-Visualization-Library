""" Styles are special processors that transform an evaluation into CSS styles. """
from matplotlib.colors import Colormap
from ftpvl.evaluation import Evaluation
from ftpvl.processors import Processor
from ftpvl.helpers import get_styling


class Style(Processor):
    """
    Represents a type of processor that returns an evaluation containing CSS
    styles for visualization.
    """

    def process(self, input_eval: Evaluation) -> Evaluation:
        raise NotImplementedError


class ColorMapStyle(Style):
    """
    Represents a processor that uses a matplotlib Colormap to create a styled
    evaluation where the background of a cell is specified by the value in the
    cell evaluated by the colormap.

    Values in the input are expected to be either a float between 0 and 1
    (inclusive) or a empty string.

    Parameters
    ----------
    cmap : Colormap
        the colormap to use when transforming input Evaluation to CSS styles.
    """

    def __init__(self, cmap: Colormap):
        self.cmap = cmap

    def process(self, input_eval: Evaluation) -> Evaluation:
        df = input_eval.get_df()
        new_df = df.applymap(lambda x: get_styling(x, self.cmap))
        return Evaluation(new_df)
