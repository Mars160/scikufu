# SciKuFu

A Python toolkit for scientific computing featuring parallel processing and statistical analysis capabilities.

## Features

### 🔄 Parallel Module (`scikufu.parallel`)

- **OpenAI Integration**: Parallel async processing for OpenAI API calls with caching support
- Batched requests with configurable concurrency
- Built-in retry logic and error handling
- Progress tracking with tqdm
- Result caching using diskcache for efficient repeated operations

### 📊 Statistics Module (`scikufu.stats`)

- **T-Test Implementation**: Comprehensive t-test with normality checks
  - Student's t-test (equal variance)
  - Welch's t-test (unequal variance)
  - PP (Probability-Probability) plots for normality visualization
  - QQ (Quantile-Quantile) plots for distribution analysis
  - Support for various data formats (tuples, DataFrames, NumPy arrays)

## Installation

### Requirements

- Python >= 3.12

### Core Installation

```bash
pip install scikufu
```

### Optional Dependencies

#### Parallel Module

```bash
pip install "scikufu[parallel]"
```

#### OpenAI Integration

```bash
pip install "scikufu[parallel-openai]"
```

#### Statistics Module

```bash
pip install "scikufu[stats]"
```

#### Full Installation

```bash
pip install "scikufu[parallel,parallel-openai,stats]"
```

## Usage

### Parallel OpenAI API Calls

```python
from scikufu.parallel.openai import Client

# Initialize client
client = Client(api_key="your-api-key")

# Prepare messages
messages = [
    [{"role": "user", "content": "What is Python?"}],
    [{"role": "user", "content": "What is JavaScript?"}],
]

# Run parallel completions
results = client.chat_completion(
    messages=messages,
    model="gpt-4",
    n_jobs=4,  # Number of parallel workers
    with_tqdm=True,  # Show progress bar
    temperature=0.7
)
```

### Statistical T-Test

```python
from scikufu.stats.ttest import t_test
import numpy as np

# Generate sample data
group1 = np.random.normal(100, 15, 30)
group2 = np.random.normal(105, 15, 30)

# Perform t-test
t_stat, p_value, significant = t_test(
    data=(group1, group2),
    alpha=0.05,
    show_plot=True,
    save_path="./t_test_plot.png"
)

print(f"t-statistic: {t_stat}")
print(f"p-value: {p_value}")
print(f"Significant: {significant}")
```

## Development

### Setup Development Environment

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Run tests with coverage
pytest
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=scikufu --cov-report=html
```

## Project Structure

```
scikufu/
├── parallel/          # Parallel processing utilities
│   ├── openai.py      # OpenAI API client for parallel requests
│   └── __init__.py
├── stats/             # Statistical analysis tools
│   ├── ttest.py       # T-test implementation
│   └── __init__.py
└── __init__.py
```

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
