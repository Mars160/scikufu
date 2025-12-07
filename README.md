# SciKuFu

[中文](./README.zh.md)

SciKuFu is a Python toolkit that wraps up the most frequently used utilities from my personal research workflow. It aims to boost productivity and simplify common scientific computing and data analysis tasks.

## Features

- **Parallel Processing**: High-performance parallel computing with threading, multiprocessing, and asyncio backends
- **OpenAI Integration**: Batch processing of OpenAI API calls with caching and structured output parsing
- **File I/O Operations**: Unified text, JSON, and JSON Lines file operations with encoding support
- **Statistical Analysis**: Comprehensive statistical methods including t-tests with normality checks and visualization
- **Clean Architecture**: Modular design with optional dependencies for lightweight core usage

## Installation

### Basic Installation

```bash
pip install scikufu
```

### With Optional Features

```bash
# Install with parallel processing and OpenAI support
pip install scikufu[parallel,parallel-openai]

# Install with statistical analysis support
pip install scikufu[stats]

# Install with all features
pip install scikufu[parallel,parallel-openai,stats]
```

### From Source

```bash
git clone https://github.com/Mars160/scikufu.git
cd scikufu
pip install -e .
```

## Quick Start

### Parallel Processing

```python
from scikufu.parallel import run_in_parallel

def process_item(item):
    return item * 2

items = [1, 2, 3, 4, 5]
results = run_in_parallel(
    func=process_item,
    tasks=items,
    n_jobs=4,
    backend="threading"  # or "multiprocessing", "asyncio"
)
print(results)  # [2, 4, 6, 8, 10]
```

### OpenAI API Batch Processing

```python
from scikufu.parallel.openai import Client

client = Client(api_key="your-api-key")
messages = [
    [{"role": "user", "content": "What is Python?"}],
    [{"role": "user", "content": "What is JavaScript?"}],
]

# Simple chat completion
results = client.chat_completion(
    messages=messages,
    model="gpt-4",
    n_jobs=4,
    with_tqdm=True,
    temperature=0.7
)

# Structured output parsing with Pydantic
from pydantic import BaseModel

class Answer(BaseModel):
    language: str
    description: str

structured_results = client.chat_completion_parse(
    messages=messages,
    model="gpt-4",
    response_model=Answer,
    n_jobs=4
)
```

### File I/O Operations

```python
from scikufu.file import text, json, jsonl

# Text file operations
text.write("hello.txt", "Hello, World!")
content = text.read("hello.txt", encoding="utf-8")

# JSON file operations
data = {"name": "SciKuFu", "version": "0.1.0"}
json.write("config.json", data, indent=4)
loaded_data = json.read("config.json")

# JSON Lines operations
records = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
jsonl.write("data.jsonl", records)
for record in jsonl.read("data.jsonl"):
    print(record)
```

### Statistical Analysis

```python
from scikufu.stats.ttest import t_test
import numpy as np

# Generate sample data
group1 = np.random.normal(100, 15, 30)
group2 = np.random.normal(105, 15, 30)

# Comprehensive t-test with visualization
t_stat, p_value, significant = t_test(
    data=(group1, group2),
    alpha=0.05,
    show_plot=True,
    save_path="./t_test_plot.png",
    test_type="welch"  # or "student"
)

print(f"t-statistic: {t_stat}")
print(f"p-value: {p_value}")
print(f"Significant: {significant}")
```

## Modules

### 🚀 Parallel Processing (`scikufu.parallel`)
- **Core Functions**: `run_in_parallel()`, `run_async_in_parallel()`
- **Backends**: Threading, Multiprocessing, AsyncIO
- **Features**: Disk-based caching, retry mechanisms, progress tracking
- **Use Case**: CPU-bound tasks, I/O operations, concurrent API calls

### 🤖 OpenAI Integration (`scikufu.parallel.openai`)
- **Client Class**: Wrapper for OpenAI async API
- **Features**: Batch processing, structured output parsing, caching
- **Use Case**: Large-scale language model inference, data processing

### 📁 File I/O (`scikufu.file`)
- **Text Operations**: `text.read()`, `text.write()`, `text.append()`
- **JSON Operations**: `json.read()`, `json.write()`, `json.append()`
- **JSONL Operations**: `jsonl.read()`, `jsonl.write()`, `jsonl.append()`
- **Features**: Unicode support, automatic directory creation, memory efficiency

### 📊 Statistical Analysis (`scikufu.stats`)
- **T-Test**: Comprehensive statistical testing with visualization
- **Features**: Normality checks, effect size calculation, PP/QQ plots
- **Input Formats**: Tuples, pandas DataFrames, numpy arrays
- **Export**: Multiple plot formats, detailed statistical reports

## Optional Dependencies

```bash
# Parallel processing features
pip install diskcache tqdm

# OpenAI API integration
pip install openai

# Statistical analysis and visualization
pip install matplotlib numpy pandas scipy
```

## Project Structure

```
scikufu/
├── src/scikufu/          # Main package source
│   ├── parallel/         # Parallel processing utilities
│   ├── openai.py        # OpenAI API integration
│   ├── file/            # File I/O operations
│   ├── stats/           # Statistical analysis
│   └── py.typed        # Type annotations support
├── tests/               # Comprehensive test suite
│   ├── parallel/       # Parallel processing tests
│   ├── file/          # File I/O tests
│   └── stats/         # Statistical tests
└── htmlcov/           # Coverage reports
```

## Requirements

- **Python**: 3.12+
- **Core Dependencies**: None (lightweight design)
- **Optional Dependencies**: Feature-based extras for specific functionality

## License

MIT

## Contributing

All features are developed based on actual research needs. Suggestions, feedback, and contributions are welcome! Please feel free to open issues or submit pull requests.

## Note

This toolkit is designed to be modular and extensible. Each module can be used independently, and the core functionality remains lightweight with optional dependencies for specific features.