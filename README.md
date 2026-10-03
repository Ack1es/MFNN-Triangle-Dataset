# MFNN Triangle Dataset

[中文说明](README.zh-CN.md)

A synthetic dataset of 10,000 triangles and the standalone code used to construct it. This repository accompanies **Mutual Feedback Neural Network for Implicit Systems: Framework, Validation, and Application** and shares only the triangle dataset construction.

Repository: https://github.com/Ack1es/MFNN-Triangle-Dataset

**Scope:** dataset generation, complete triangle parameters, and documentation. No prediction models, training procedures, train/validation/test partitions, normalization, evaluation results, or TBM engineering data are included.

## Repository Structure

```text
MFNN-Triangle-Dataset/
├── README.md
├── README.zh-CN.md
├── CITATION.cff
├── .gitignore
├── requirements.txt
├── generate_dataset.py
├── docs/
│   └── dataset-construction.md
└── data/
    ├── triangle_clean_seed42_n10000.npz
    ├── triangle_clean_seed42_n10000.csv
    ├── data_dictionary.csv
    └── metadata.json
```

## Dataset Overview

| Item | Value |
| --- | --- |
| Samples | 10,000 triangles |
| Random seed | 42 |
| Parameter order | `a, b, theta_ab, theta_b, c, theta_c` |
| Stored parameter type | `float32` |
| Side-length unit | Synthetic length unit; not metres |
| Angle unit | Radian |
| Missing values | None |
| Formats | NumPy NPZ and CSV |

The generator independently samples two side lengths and their included angle, then derives the remaining side and angles from triangle geometry. The supplied NPZ is the original cached dataset; the CSV is an equivalent readable export, with the original row order and numerical values preserved.

## Installation

The generation procedure was verified with Python 3.11 and NumPy 1.26.4.

```shell
python -m pip install -r requirements.txt
```

No GPU, machine-learning framework, or additional data download is required.

## Generate Data

From the repository root:

```shell
python generate_dataset.py --samples 10000 --seed 42
```

This creates NPZ, CSV, and metadata files in `generated_data/`, leaving the supplied `data/` files unchanged. To use a different output directory:

```shell
python generate_dataset.py --samples 10000 --seed 42 --output-dir my_data
```

With the documented environment, the default sample count and seed reproduce the supplied parameter array. A regenerated NPZ file need not be byte-identical because its archive metadata can differ.

## Load Data

### NumPy

```python
import numpy as np

with np.load("data/triangle_clean_seed42_n10000.npz") as dataset:
    triangles = dataset["clean"]
    seed = int(dataset["seed"])
    samples = int(dataset["samples"])

print(triangles.shape)  # (10000, 6)
a, b, theta_ab, theta_b, c, theta_c = triangles.T
```

### CSV

```python
import numpy as np

records = np.genfromtxt(
    "data/triangle_clean_seed42_n10000.csv",
    delimiter=",",
    names=True,
)
sample_index = records["sample_index"].astype(int)
included_angles = records["theta_ab"]
```

The CSV includes an additional zero-based `sample_index`; it is a row identifier, not a geometric parameter. See [the data dictionary](data/data_dictionary.csv) for field definitions and [the construction notes](docs/dataset-construction.md) for sampling ranges, formulas, and numerical details.

## Citation

Citation metadata for this dataset are provided in [CITATION.cff](CITATION.cff). The associated manuscript is:

Wang, L.-c., Li, X., & Chen, Z.-y. *Mutual Feedback Neural Network for Implicit Systems: Framework, Validation, and Application*.

The dataset repository URL is recorded in `CITATION.cff`. Publication details for the associated manuscript are not yet recorded. No journal acceptance, publication year, or DOI is implied by this citation.

## License

A distribution license has not yet been selected. Public visibility alone does not grant permission to reuse or redistribute the code or data. This section will be updated after the authors confirm the license.
