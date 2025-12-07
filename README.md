# SciKuFu

[中文](./README.zh.md)

SciKuFu is a Python toolkit that wraps up the most frequently used utilities from my personal research workflow. It aims to boost productivity and simplify common scientific computing and data analysis tasks.

## Features

- Parallel computing and batch processing (e.g., concurrent OpenAI API requests, result caching)
- Common statistical analysis methods (e.g., t-test, normality checks, visualization)
- Clean code structure, easy to extend and integrate into personal projects

## Installation

Recommended:

```bash
pip install scikufu
```

Or from source:

```bash
git clone https://github.com/Mars160/scikufu.git
cd scikufu
pip install .
```

## Quick Start

### Parallel OpenAI API Calls

```python
from scikufu.parallel.openai import Client

client = Client(api_key="your-api-key")
messages = [
    [{"role": "user", "content": "What is Python?"}],
    [{"role": "user", "content": "What is JavaScript?"}],
]
results = client.chat_completion(
    messages=messages,
    model="gpt-4",
    n_jobs=4,
    with_tqdm=True,
    temperature=0.7
)
```

### Statistical T-Test

```python
from scikufu.stats.ttest import t_test
import numpy as np

group1 = np.random.normal(100, 15, 30)
group2 = np.random.normal(105, 15, 30)
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

## Project Structure

- `src/scikufu/`: main code
- `tests/`: test code
- `htmlcov/`: coverage report

## License

MIT

## Note

All features are developed based on my own research needs. Suggestions and feedback are welcome!
