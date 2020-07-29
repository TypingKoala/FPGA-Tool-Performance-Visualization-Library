""" Implement tests for Visualizer class"""
import pandas as pd
import pytest
import seaborn as sns

from ftpvl.evaluation import Evaluation
from ftpvl.styles import ColorMapStyle
from ftpvl.visualizers import DebugVisualizer, SingleTableVisualizer


class TestVisualizer():
    """
    Testing by partition.

    DebugVisualizer()

    SingleTableVisualizer()
    """
    def test_debugvisualizer(self):
        """Test for raised exceptions when valid inputs"""
        df = pd.DataFrame(
            [
                {"a": 0.1, "b": 0.2, "c": 0.3},
                {"a": 0.4, "b": 0.5, "c": 0.6},
                {"a": 0.7, "b": 0.8, "c": 0.9},
            ]
        )
        eval1 = Evaluation(df)
        vis = DebugVisualizer(eval1, column_order=["a", "b", "c"])
        vis.get_visualization() # should not fail

        with pytest.raises(KeyError):
            vis = DebugVisualizer(eval1, column_order=["d"])
            vis.get_visualization()

    def test_singletablevisualizer(self):
        df = pd.DataFrame(
            [
                {"a": 0.1, "b": 0.2, "c": 0.3},
                {"a": 0.4, "b": 0.5, "c": 0.6},
                {"a": 0.7, "b": 0.8, "c": 0.9},
            ]
        )
        eval1 = Evaluation(df)
        cmap = sns.diverging_palette(180, 0, s=75, l=75, sep=100, as_cmap=True)
        styled_eval = eval1.process([ColorMapStyle(cmap)])
        vis = SingleTableVisualizer(eval1, styled_eval, column_order=["a", "b", "c"])
        vis.get_visualization() # should not fail

        with pytest.raises(KeyError):
            vis = SingleTableVisualizer(eval1, styled_eval, column_order=["d"])
            vis.get_visualization()
