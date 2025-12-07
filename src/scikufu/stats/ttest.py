"""
T-test implementation with normality checks and visualization.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
from pathlib import Path
from typing import Tuple, Union, Sequence, Optional


def t_test(
    data: Union[
        Tuple[Sequence[int], Sequence[int]],
        pd.DataFrame,
        np.ndarray
    ],
    alpha: float = 0.05,
    save_path: Optional[Union[str, Path]] = None,
    show_plot: bool = True,
    equal_var: bool = True,
    test_type: str = "two-sided"
) -> Tuple[float, float, bool]:
    """
    Perform t-test with normality checks (PP and QQ plots).

    Parameters:
    -----------
    data : tuple, pd.DataFrame, or np.ndarray
        Input data in one of the following formats:
        - tuple of two sequences: (group1, group2)
        - pd.DataFrame with exactly two columns
        - np.ndarray with shape (2, n) or (n, 2)
    alpha : float, default 0.05
        Significance level for the test
    save_path : str or Path, optional
        Path to save the plots. If None, plots are not saved.
    show_plot : bool, default True
        Whether to display the plots
    equal_var : bool, default True
        If True, perform Student's t-test (assume equal variance).
        If False, perform Welch's t-test (unequal variance).
    test_type : str, default "two-sided"
        Type of test: "two-sided", "less", or "greater"

    Returns:
    --------
    tuple : (t_statistic, p_value, significant)
        t_statistic : float
            The computed t-statistic
        p_value : float
            The two-tailed p-value
        significant : bool
            Whether the result is significant at the given alpha level
    """

    # Parse input data
    group1, group2 = _parse_data(data)

    # Convert to numpy arrays
    group1 = np.asarray(group1, dtype=float)
    group2 = np.asarray(group2, dtype=float)

    # Remove NaN values
    group1 = group1[~np.isnan(group1)]
    group2 = group2[~np.isnan(group2)]

    # Check for sufficient data
    if len(group1) < 2 or len(group2) < 2:
        raise ValueError("Each group must have at least 2 non-NaN observations")

    # Create figure for normality checks
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Normality Checks and T-Test Results', fontsize=16)

    # PP plot for group 1
    _create_pp_plot(group1, ax1, f'Group 1 (n={len(group1)})')

    # QQ plot for group 1
    _create_qq_plot(group1, ax2, f'Group 1 QQ Plot')

    # PP plot for group 2
    _create_pp_plot(group2, ax3, f'Group 2 (n={len(group2)})')

    # QQ plot for group 2
    _create_qq_plot(group2, ax4, f'Group 2 QQ Plot')

    plt.tight_layout()

    # Save plots if requested
    if save_path is not None:
        save_path = Path(save_path)
        if save_path.suffix == '':
            save_path = save_path / 'ttest_normality_checks.png'
        elif save_path.suffix.lower() not in ['.png', '.jpg', '.jpeg', '.pdf', '.svg']:
            save_path = save_path.with_suffix('.png')

        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plots saved to: {save_path}")

    # Show plots if requested
    if show_plot:
        plt.show()
    else:
        plt.close()

    # Perform t-test
    if equal_var:
        t_stat, p_value = stats.ttest_ind(group1, group2, alternative=test_type)
        test_name = "Student's t-test"
    else:
        t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False, alternative=test_type)
        test_name = "Welch's t-test"

    # Determine significance
    significant = bool(p_value < alpha)

    # Print results
    print(f"\n{test_name} Results:")
    print(f"Group 1: n={len(group1)}, mean={np.mean(group1):.4f}, std={np.std(group1, ddof=1):.4f}")
    print(f"Group 2: n={len(group2)}, mean={np.mean(group2):.4f}, std={np.std(group2, ddof=1):.4f}")
    print(f"t-statistic: {t_stat:.4f}")
    print(f"p-value: {p_value:.6f}")
    print(f"Significant at α={alpha}: {significant}")

    # Effect size (Cohen's d)
    pooled_std = np.sqrt(((len(group1) - 1) * np.var(group1, ddof=1) +
                         (len(group2) - 1) * np.var(group2, ddof=1)) /
                        (len(group1) + len(group2) - 2))
    cohens_d = (np.mean(group1) - np.mean(group2)) / pooled_std
    print(f"Cohen's d: {cohens_d:.4f}")

    return t_stat, p_value, significant


def _parse_data(data) -> Tuple[np.ndarray, np.ndarray]:
    """Parse input data into two groups."""

    if isinstance(data, tuple):
        if len(data) != 2:
            raise ValueError("Tuple input must contain exactly 2 sequences")
        group1, group2 = data

    elif isinstance(data, pd.DataFrame):
        if data.shape[1] != 2:
            raise ValueError("DataFrame must have exactly 2 columns")
        group1, group2 = data.iloc[:, 0].values, data.iloc[:, 1].values

    elif isinstance(data, np.ndarray):
        if data.ndim == 1:
            if len(data) != 2:
                raise ValueError("1D array must have exactly 2 elements")
            raise ValueError("1D array input not supported. Use 2D array instead.")
        elif data.ndim == 2:
            if data.shape[0] == 2:
                group1, group2 = data[0, :], data[1, :]
            elif data.shape[1] == 2:
                group1, group2 = data[:, 0], data[:, 1]
            else:
                raise ValueError("2D array must have shape (2, n) or (n, 2)")
        else:
            raise ValueError("Array must be 1D or 2D")

    else:
        raise TypeError("Data must be tuple, pandas DataFrame, or numpy array")

    return group1, group2


def _create_pp_plot(data: np.ndarray, ax, title: str):
    """Create a P-P plot for the data."""

    # Sort the data
    sorted_data = np.sort(data)
    n = len(sorted_data)

    # Calculate empirical cumulative probabilities
    empirical_probs = np.arange(1, n + 1) / (n + 1)

    # Calculate theoretical quantiles from normal distribution
    mean, std = np.mean(data), np.std(data, ddof=1)
    theoretical_probs = stats.norm.cdf(sorted_data, mean, std)

    # Create P-P plot
    ax.scatter(theoretical_probs, empirical_probs, alpha=0.6, s=30)
    ax.plot([0, 1], [0, 1], 'r--', lw=2, label='y = x')

    # Add labels and title
    ax.set_xlabel('Theoretical Cumulative Probability')
    ax.set_ylabel('Empirical Cumulative Probability')
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend()

    # Set axis limits
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)


def _create_qq_plot(data: np.ndarray, ax, title: str):
    """Create a Q-Q plot for the data."""

    # Create Q-Q plot
    stats.probplot(data, dist="norm", plot=ax)

    # Customize plot
    ax.set_title(title)
    ax.grid(True, alpha=0.3)

    # Add correlation coefficient for linearity
    qq_data = stats.probplot(data, dist="norm", rvalue=True)
    r_value = qq_data[1][2]
    ax.text(0.05, 0.95, f'R² = {r_value**2:.4f}',
            transform=ax.transAxes, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))