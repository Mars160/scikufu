# SciKuFu

[English](./README.md)

SciKuFu 是一个将我个人科研过程中常用功能进行封装的 Python 工具包，旨在提升科研效率，简化常见的科学计算和数据分析任务。

## 主要功能

- **并行处理**：高性能并行计算，支持线程、进程和异步 IO 后端
- **OpenAI 集成**：批量处理 OpenAI API 调用，支持缓存和结构化输出解析
- **文件 I/O 操作**：统一的文本、JSON 和 JSON Lines 文件操作，支持编码
- **统计分析**：全面的统计方法，包括带正态性检验和可视化的 t 检验
- **清晰架构**：模块化设计，可选依赖，轻量级核心使用

## 安装方法

### 基础安装

```bash
pip install scikufu
```

### 带可选功能的安装

```bash
# 安装并行处理和 OpenAI 支持
pip install scikufu[parallel,parallel-openai]

# 安装统计分析支持
pip install scikufu[stats]

# 安装所有功能
pip install scikufu[parallel,parallel-openai,stats]
```

### 源码安装

```bash
git clone https://github.com/Mars160/scikufu.git
cd scikufu
pip install -e .
```

## 快速开始

### 并行处理

```python
from scikufu.parallel import run_in_parallel

def process_item(item):
    return item * 2

items = [1, 2, 3, 4, 5]
results = run_in_parallel(
    tasks=process_item,
    args_=[(item,) for item in items],
    n_jobs=4,
    thread=True  # 或 process=True，或不填使用 asyncio
)
print(results)  # [2, 4, 6, 8, 10]
```

### OpenAI API 批量处理

```python
from scikufu.parallel.openai import Client

client = Client(api_key="你的API密钥")
messages = [
    [{"role": "user", "content": "什么是Python?"}],
    [{"role": "user", "content": "什么是JavaScript?"}],
]

# 简单聊天完成
results = client.chat_completion(
    messages=messages,
    model="gpt-4",
    n_jobs=4,
    with_tqdm=True,
    temperature=0.7
)

# 使用 Pydantic 进行结构化输出解析
from pydantic import BaseModel

class Answer(BaseModel):
    language: str
    description: str

structured_results = client.chat_completion_parse(
    messages=messages,
    model="gpt-4",
    response_format=Answer,
    n_jobs=4
)
```

### 文件 I/O 操作

```python
from scikufu.file import text, json, jsonl

# 文本文件操作
text.write("hello.txt", "你好，世界！")
content = text.read("hello.txt", encoding="utf-8")

# JSON 文件操作
data = {"name": "SciKuFu", "version": "0.1.0"}
json.write("config.json", data, indent=4)
loaded_data = json.read("config.json")

# JSON Lines 操作
records = [{"id": 1, "name": "张三"}, {"id": 2, "name": "李四"}]
jsonl.write("data.jsonl", records)
# jsonl.read() 返回生成器
for record in jsonl.read("data.jsonl"):
    print(record)
# 或转换为列表：records = list(jsonl.read("data.jsonl"))
```

### 统计分析

```python
from scikufu.stats.ttest import t_test
import numpy as np

# 生成样本数据
group1 = np.random.normal(100, 15, 30)
group2 = np.random.normal(105, 15, 30)

# 带可视化的全面 t 检验
t_stat, p_value, significant = t_test(
    data=(group1, group2),
    alpha=0.05,
    show_plot=True,
    save_path="./t_test_plot.png",
    equal_var=False  # False 为 Welch t-test，True 为 Student t-test
)

print(f"t统计量: {t_stat}")
print(f"p值: {p_value}")
print(f"显著性: {significant}")
```

## 模块介绍

### 🚀 并行处理 (`scikufu.parallel`)

- **核心函数**：`run_in_parallel()`, `run_async_in_parallel()`
- **后端支持**：线程、进程、异步 IO
- **特色功能**：磁盘缓存、重试机制、进度跟踪
- **使用场景**：CPU 密集型任务、I/O 操作、并发 API 调用

### 🤖 OpenAI 集成 (`scikufu.parallel.openai`)

- **客户端类**：OpenAI 异步 API 封装
- **特色功能**：批量处理、结构化输出解析、缓存
- **使用场景**：大规模语言模型推理、数据处理

### 📁 文件 I/O (`scikufu.file`)

- **文本操作**：`text.read()`, `text.write()`, `text.append()`
- **JSON 操作**：`json.read()`, `json.write()`, `json.append()`
- **JSONL 操作**：`jsonl.read()`, `jsonl.write()`, `jsonl.append()`
- **特色功能**：Unicode 支持、自动目录创建、内存高效

### 📊 统计分析 (`scikufu.stats`)

- **T 检验**：带可视化的全面统计检验
- **特色功能**：正态性检验、效应量计算、PP/QQ 图
- **输入格式**：元组、pandas DataFrame、numpy 数组
- **导出功能**：多种图表格式、详细统计报告

## 可选依赖

```bash
# 并行处理功能
pip install diskcache tqdm

# OpenAI API 集成
pip install openai

# 统计分析和可视化
pip install matplotlib numpy pandas scipy
```

## 项目结构

```
scikufu/
├── src/scikufu/          # 主包源码
│   ├── parallel/         # 并行处理工具
│   ├── openai.py        # OpenAI API 集成
│   ├── file/            # 文件 I/O 操作
│   ├── stats/           # 统计分析
│   └── py.typed        # 类型注解支持
├── tests/               # 全面测试套件
│   ├── parallel/       # 并行处理测试
│   ├── file/          # 文件 I/O 测试
│   └── stats/         # 统计测试
└── htmlcov/           # 覆盖率报告
```

## 系统要求

- **Python**：3.12+
- **核心依赖**：无（轻量级设计）
- **可选依赖**：基于功能的可选依赖，用于特定功能

## 许可证

MIT

## 贡献

所有功能都基于实际的科研需求开发。建议、反馈和贡献都欢迎！请随时提出 Issue 或提交 Pull Request。

## 说明

本工具包设计为模块化和可扩展的。每个模块都可以独立使用，核心功能保持轻量级，特定功能有可选依赖。
