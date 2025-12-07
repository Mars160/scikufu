"""
Tests for the t-test function.
"""

import numpy as np
import pandas as pd
import pytest
from unittest.mock import patch
from pathlib import Path
import tempfile

from scikufu.stats import t_test


class TestTTest:
    """Test cases for the t_test function."""

    def setup_method(self):
        """Set up test data."""
        np.random.seed(42)
        # Create test data from normal distributions
        self.group1 = np.random.normal(10, 2, 50)
        self.group2 = np.random.normal(12, 2, 50)
        self.temp_dir = tempfile.mkdtemp()

    def test_tuple_input(self):
        """Test with tuple input."""
        data = (self.group1, self.group2)
        t_stat, p_value, significant = t_test(data, show_plot=False)

        assert isinstance(t_stat, float)
        assert isinstance(p_value, float)
        assert isinstance(significant, bool)
        assert 0 <= p_value <= 1

    def test_dataframe_input(self):
        """Test with DataFrame input."""
        df = pd.DataFrame({'group1': self.group1, 'group2': self.group2})
        t_stat, p_value, significant = t_test(df, show_plot=False)

        assert isinstance(t_stat, float)
        assert isinstance(p_value, float)
        assert isinstance(significant, bool)

    def test_numpy_array_2xn(self):
        """Test with numpy array of shape (2, n)."""
        data = np.array([self.group1, self.group2])
        t_stat, p_value, significant = t_test(data, show_plot=False)

        assert isinstance(t_stat, float)
        assert isinstance(p_value, float)
        assert isinstance(significant, bool)

    def test_numpy_array_nx2(self):
        """Test with numpy array of shape (n, 2)."""
        data = np.column_stack([self.group1, self.group2])
        t_stat, p_value, significant = t_test(data, show_plot=False)

        assert isinstance(t_stat, float)
        assert isinstance(p_value, float)
        assert isinstance(significant, bool)

    def test_invalid_tuple_length(self):
        """Test error handling for invalid tuple length."""
        with pytest.raises(ValueError, match="Tuple input must contain exactly 2 sequences"):
            t_test((self.group1,), show_plot=False)

        with pytest.raises(ValueError, match="Tuple input must contain exactly 2 sequences"):
            t_test((self.group1, self.group2, self.group1), show_plot=False)

    def test_invalid_dataframe_columns(self):
        """Test error handling for DataFrame with wrong number of columns."""
        df_single = pd.DataFrame({'group1': self.group1})
        with pytest.raises(ValueError, match="DataFrame must have exactly 2 columns"):
            t_test(df_single, show_plot=False)

        df_triple = pd.DataFrame({
            'group1': self.group1,
            'group2': self.group2,
            'group3': self.group1
        })
        with pytest.raises(ValueError, match="DataFrame must have exactly 2 columns"):
            t_test(df_triple, show_plot=False)

    def test_invalid_numpy_array_shape(self):
        """Test error handling for invalid numpy array shapes."""
        # 3D array
        arr_3d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        with pytest.raises(ValueError, match="Array must be 1D or 2D"):
            t_test(arr_3d, show_plot=False)

        # 2D array with wrong shape
        arr_wrong = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        with pytest.raises(ValueError, match="2D array must have shape \\(2, n\\) or \\(n, 2\\)"):
            t_test(arr_wrong, show_plot=False)

    def test_insufficient_data(self):
        """Test error handling for insufficient data."""
        # Single observations
        with pytest.raises(ValueError, match="Each group must have at least 2 non-NaN observations"):
            t_test(([1], [2]), show_plot=False)

        # Empty groups
        with pytest.raises(ValueError, match="Each group must have at least 2 non-NaN observations"):
            t_test(([], []), show_plot=False)

    def test_nan_handling(self):
        """Test handling of NaN values."""
        group1_with_nan = np.array([1, 2, np.nan, 4, 5])
        group2_with_nan = np.array([3, np.nan, 5, 6, 7])

        t_stat, p_value, significant = t_test(
            (group1_with_nan, group2_with_nan), show_plot=False
        )

        assert isinstance(t_stat, float)
        assert isinstance(p_value, float)
        assert isinstance(significant, bool)

    def test_welch_ttest(self):
        """Test Welch's t-test (unequal variance assumption)."""
        # Create groups with different variances
        group1 = np.random.normal(10, 1, 50)
        group2 = np.random.normal(12, 3, 50)

        # Test with equal variance assumption
        t_eq, p_eq, sig_eq = t_test((group1, group2), equal_var=True, show_plot=False)

        # Test with unequal variance assumption (Welch)
        t_welch, p_welch, sig_welch = t_test((group1, group2), equal_var=False, show_plot=False)

        assert t_eq != t_welch or p_eq != p_welch  # Results should be different

    def test_save_plots(self):
        """Test saving plots to file."""
        save_path = Path(self.temp_dir) / "test_plot.png"

        # Mock plt.show to prevent actual display during test
        with patch('matplotlib.pyplot.show'):
            t_test((self.group1, self.group2),
                  save_path=save_path, show_plot=False)

        assert save_path.exists()
        assert save_path.stat().st_size > 0

    def test_identical_groups(self):
        """Test with identical groups (should have p-value close to 1)."""
        identical_data = np.random.normal(10, 2, 50)
        t_stat, p_value, significant = t_test(
            (identical_data, identical_data), show_plot=False
        )

        assert abs(t_stat) < 1.0  # t-statistic should be close to 0
        assert p_value > 0.5  # p-value should be close to 1
        assert not significant  # Should not be significant

    def test_invalid_input_type(self):
        """Test error handling for invalid input types."""
        with pytest.raises(TypeError, match="Data must be tuple, pandas DataFrame, or numpy array"):
            t_test("invalid_input", show_plot=False)

        with pytest.raises(TypeError, match="Data must be tuple, pandas DataFrame, or numpy array"):
            t_test(123, show_plot=False)

        with pytest.raises(TypeError, match="Data must be tuple, pandas DataFrame, or numpy array"):
            t_test([1, 2, 3], show_plot=False)