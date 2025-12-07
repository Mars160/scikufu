# Scikufu

[English](./README.md)

Scikufu 是一个将我个人科研过程中常用功能进行封装的 Python 工具包，旨在提升科研效率，简化常见的数据处理和分析流程。

## 主要功能

- 并行计算与批量处理（如 OpenAI API 并发请求、结果缓存等）
- 常用统计分析方法（如 t 检验、正态性检验、可视化等）
- 代码结构清晰，易于扩展和集成到个人项目

## 安装方法

推荐使用 pip 安装：

```bash
pip install scikufu
```

或源码安装：

```bash
git clone https://github.com/Mars160/scikufu.git
cd scikufu
pip install .
```

## 快速开始

### 并行 OpenAI API 请求

```python
from scikufu.parallel.openai import Client

client = Client(api_key="你的API密钥")
messages = [
	[{"role": "user", "content": "什么是Python?"}],
	[{"role": "user", "content": "什么是JavaScript?"}],
]
results = client.chat_completion(
	messages=messages,
	model="gpt-4",
	n_jobs=4,
	with_tqdm=True,
	temperature=0.7
)
```

### 统计 t 检验

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
print(f"t统计量: {t_stat}")
print(f"p值: {p_value}")
print(f"显著性: {significant}")
```

## 目录结构

- `src/scikufu/`：主程序代码
- `tests/`：测试代码
- `htmlcov/`：测试覆盖率报告

## 许可证

MIT

## 说明

本项目所有功能均为个人科研实际需求所开发，欢迎有类似需求的朋友交流或提出建议。

## 许可证

本项目采用 MIT 许可证。

## 联系方式

如有问题或建议，请通过 GitHub Issues 联系我们。
