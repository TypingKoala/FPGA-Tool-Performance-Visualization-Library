""" This module defines visualizers for ftpvl """

from ftpvl import Evaluation, Style

class Visualizer():
    """
    Represents a visualizer that can generate and display styled evaluations.

    Methods:
        get_visualization(): returns a displayable visualizaton, can be
            displayed by calling display() in an interactive Python environment
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
        Returns a displayable object using IPython display.
        """
        self._generate()
        return self._visualization

class DebugVisualizer(Visualizer):
    """
    Represents a visualizer that will print the given Evaluation, possibly with
    version information.

    Useful for debugging.

    Attributes:
        evaluation: an Evaluation to display
        version_info: a boolean flag that will show version info if True
    """
    def __init__(self, evaluation: Evaluation, version_info: bool = False):
        super().__init__()
        self._evaluation = evaluation
        self._version_info = version_info

    def _generate(self):
        # TODO: Implement visualization generation
        raise NotImplementedError

class SingleTableVisualizer(Visualizer):
    """
    Represents a visualizer for a styled single table.
    """
    def __init__(self, evaluation: Evaluation, style: Style,
                 version_info: bool = False):
        super().__init__()
        self._evaluation = evaluation
        self._style = style
        self._version_info = version_info

    def _generate(self):
        # TODO: Implement visualization generation
        raise NotImplementedError

# class TwoTableVisualizer(Visualizer):
#     """
#     Represents a visualizer for a styled double table.
#     """
#     def __init__(self, evaluation1: Evaluation, evaluation2: Evaluation,
#                  style: Style, version_info: bool = False):
#         super().__init__()
#         self._evaluation1 = evaluation1
#         self._evaluation2 = evaluation2
#         self._style = style
#         self._version_info = version_info

#     def _generate(self):
#         # TODO: Implement visualization generation
#         raise NotImplementedError
