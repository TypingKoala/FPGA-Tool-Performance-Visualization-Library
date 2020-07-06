""" Implement tests for Visualizer class"""
import pandas as pd
import pytest

from ftpvl.evaluation import Evaluation
from ftpvl.visualizers import DebugVisualizer
class TestVisualizer():
    """
    Testing by partition.

    DebugVisualizer()

    SingleTableVisualizer()

    TwoTableVisualizer()

    """
    def test_debugvisualizer(self):
        """
                evaluation: Evaluation,
        version_info: bool = False,
        custom_styles: List[dict] = None,
        column_order: List[str] = None,
        """
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
        pass

    def test_twotablevisualizer(self):
        pass
