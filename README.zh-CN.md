# MFNN 三角形数据集

[English](README.md)

本仓库提供 **10,000 个合成三角形的数据及其构建代码**，对应论文 *Mutual Feedback Neural Network for Implicit Systems: Framework, Validation, and Application* 中的几何数据集构建部分。

仓库地址：https://github.com/Ack1es/MFNN-Triangle-Dataset

## 共享范围

仅包含数据生成代码、完整的三角形参数、字段说明和生成原理。**不包含预测模型、训练流程、训练/验证/测试集划分、归一化、评价结果或 TBM 工程数据。**

## 文件说明

| 文件 | 内容 |
| --- | --- |
| `generate_dataset.py` | 独立的数据生成及导出程序 |
| `requirements.txt` | 经核对的 NumPy 依赖版本 |
| `data/triangle_clean_seed42_n10000.npz` | 原始缓存数据，未修改 |
| `data/triangle_clean_seed42_n10000.csv` | 对应的可读 CSV 数据 |
| `data/data_dictionary.csv` | 字段定义与单位 |
| `data/metadata.json` | 样本数量、种子、列顺序和构建规则 |
| `docs/dataset-construction.md` | 采样范围、几何关系和数值计算说明 |
| `CITATION.cff` | 数据集引用信息 |

## 数据概况

- 样本数量：10,000 个三角形。
- 随机种子：42。
- 参数顺序：`a, b, theta_ab, theta_b, c, theta_c`。
- 参数存储类型：`float32`。
- 边长采用合成长度单位，不代表米；角度均以弧度存储。
- CSV 额外包含从 0 开始的 `sample_index`，用于标识原始行顺序。

程序独立采样两条边长及其夹角，再通过三角形几何关系求得另一条边及另外两个角。独立采样的输入服从均匀分布，并不意味着所有三角形形状均匀分布。

## 安装与生成

已使用 Python 3.11 和 NumPy 1.26.4 核对数据构建，无需 GPU 或深度学习框架。

在仓库根目录执行：

```shell
python -m pip install -r requirements.txt
python generate_dataset.py --samples 10000 --seed 42
```

新生成的数据保存到 `generated_data/`，不会覆盖仓库自带的 `data/`。也可以指定其他输出目录：

```shell
python generate_dataset.py --samples 10000 --seed 42 --output-dir my_data
```

在所述环境中，默认样本数量与种子可复现提供的参数数组。NPZ 压缩文件自身的字节内容可能因压缩包元数据而不同，应比较其中的数组值。

## 读取数据

```python
import numpy as np

with np.load("data/triangle_clean_seed42_n10000.npz") as dataset:
    triangles = dataset["clean"]

print(triangles.shape)  # (10000, 6)
```

各列的详细定义见[字段表](data/data_dictionary.csv)，具体构建方法见[数据构建说明](docs/dataset-construction.md)。

## 引用

数据集引用信息见 [CITATION.cff](CITATION.cff)，其中已填写本仓库地址。对应论文的题目和作者信息列于英文 README 中。目前未填写论文出版信息或 DOI，不表示论文已被期刊录用或发表。

## 许可证

许可证尚未确定。仓库公开可见不等于自动授权他人使用或再分发，待作者确认后补充。
