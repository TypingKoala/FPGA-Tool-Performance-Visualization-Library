""" Visualizers are used for displaying the results to the user in an IPython notebook. """
from typing import List

from ftpvl.evaluation import Evaluation

class Visualizer:
    """
    Superclass for visualizers that can generate and display styled evaluations.
    """

    def __init__(self):
        self._visualization = None

    def _generate(self):
        """
        Generates the visualzation and writes it to self._visualization
        """
        raise NotImplementedError

    def get_visualization(self):
        """
        Returns a displayable object which can be displayed by calling display()
        in an interactive Python environment.
        """
        self._generate()
        return self._visualization


class DebugVisualizer(Visualizer):
    """
    Represents a visualizer that will print the given Evaluation, possibly with
    version information.

    Useful for debugging.

    Parameters
    ----------
    evaluation : Evaluation
        the Evaluation to display

    version_info : bool, optional
        Flag to display version information from the build results in the
        final visualization, by default False

    custom_styles : List[dict], optional
        Specify additional styling for the final visualzation. See
        formatting here:
        https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html#Table-styles,
        by default None

    column_order : List[str], optional
        Specify the columns and ordering  in the final visualization.
        Overrides version_info, so you must specify version columns in
        addition. Defaults to None, which will set the column order to a
        preset useful for VtR.

    Methods
    -------
    get_visualization() :
        returns a displayable visualizaton, can be displayed by calling
        display() in an interactive Python environment
    """

    def __init__(
        self,
        evaluation: Evaluation,
        version_info: bool = False,
        custom_styles: List[dict] = None,
        column_order: List[str] = None,
    ):
        super().__init__()
        self._evaluation = evaluation
        self._version_info = version_info
        self._custom_styles = custom_styles if custom_styles else []

        if column_order is None:
            self._column_order = []
            self._column_order += [
                "device",
                "bram",
                "carry",
                "dff",
                "iob",
                "lut",
                "pll",
                "synthesis",
                "pack",
                "place",
                "route",
                "fasm",
                "bitstream",
                "total",
                "freq",
                "normalized_max_freq",
            ]
            if self._version_info:
                self._column_order += [
                    "versions.vivado",
                    "versions.vpr",
                    "versions.yosys",
                    "versions.nextpnr-xilinx",
                    "versions.nextpnr-ice40",
                ]
        else:
            self._column_order = column_order

    def _generate(self):
        """ Generate visualization and save in self._visualization """
        ordered_df = self._evaluation.get_df()[self._column_order]

        self._visualization = (
            ordered_df.style.set_table_styles(self._custom_styles)
            .set_precision(2)
            .highlight_null("yellow")
            .set_na_rep("-")
        )
    
    def get_visualization(self):
        return super().get_visualization()


class SingleTableVisualizer(Visualizer):
    """
    Represents a visualizer for a styled single table, possibly with version
    information.

    Parameters
    ----------
    evaluation : Evaluation
        the Evaluation with values to display

    style_eval : Evaluation
        the Evaluation to use for styling. Should be processed using a
        Style, all values are valid CSS strings or empty.

    version_info : bool, optional
        Flag to display version information from the build results in the
        final visualization, by default False

    custom_styles : List[dict], optional
        Specify additional styling for the final visualzation. See
        formatting here:
        https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html#Table-styles,
        by default None

    column_order : List[str], optional
        Specify the columns and ordering in the final visualization.
        Overrides version_info, so you must specify version columns in
        addition. Defaults to None, which will set the column order to a
        preset useful for VtR.

    Methods
    -------
    get_visualization() :
        returns a displayable visualizaton, can be
        displayed by calling display() in an interactive Python environment
    """

    def __init__(
        self,
        evaluation: Evaluation,
        style_eval: Evaluation,
        version_info: bool = False,
        custom_styles: List[dict] = None,
        column_order: List[str] = None,
    ):
        super().__init__()
        self._evaluation = evaluation
        self._style_eval = style_eval
        self._version_info = version_info

        self._custom_styles = custom_styles if custom_styles else []

        if column_order is None:
            self._column_order = []
            self._column_order += [
                "bram",
                "carry",
                "dff",
                "iob",
                "lut",
                "pll",
                "synthesis",
                "pack",
                "place",
                "route",
                "fasm",
                "bitstream",
                "total",
                "freq",
                "normalized_max_freq",
            ]
            if self._version_info:
                self._column_order += [
                    "versions.vivado",
                    "versions.vpr",
                    "versions.yosys",
                    "versions.nextpnr-xilinx",
                    "versions.nextpnr-ice40",
                ]
        else:
            self._column_order = column_order

    def _generate(self):
        """ Generate visualization and save in self._visualization """
        ordered_df = self._evaluation.get_df()[self._column_order]
        styled_df = self._style_eval.get_df()[self._column_order]
        self._visualization = (
            ordered_df.style.apply(lambda x: styled_df, axis=None)
            .set_table_styles(self._custom_styles)
            .set_precision(2)
            .highlight_null("yellow")
            .set_na_rep("-")
        )

    def get_visualization(self):
        return super().get_visualization()
