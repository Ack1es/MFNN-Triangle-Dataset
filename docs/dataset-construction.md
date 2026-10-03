# Dataset Construction

## Parameters and Units

Each row contains six parameters, in this exact order:

| Parameter | Definition | Unit |
| --- | --- | --- |
| `a` | First independently sampled side length | Synthetic length unit |
| `b` | Second independently sampled side length | Synthetic length unit |
| `theta_ab` | Included angle between `a` and `b`, opposite `c` | Radian |
| `theta_b` | Interior angle opposite `b` | Radian |
| `c` | Side opposite `theta_ab` | Synthetic length unit |
| `theta_c` | Interior angle opposite `a` | Radian |

The names follow the original dataset. In particular, `theta_c` is opposite **`a`**, not `c`. The CSV contains the same six parameters plus a zero-based `sample_index`.

## Sampling

The random-number generator is `numpy.random.default_rng(seed)`. For the supplied dataset, `seed = 42` and `n_samples = 10000`.

The following inputs are independently sampled from uniform distributions:

- `a`: from 0.5 to 5.0.
- `b`: from 0.5 to 5.0.
- `theta_ab`: from pi/6 to 5*pi/6 radians, equivalent to 30 to 150 degrees.

Sampling is performed for all `a` values first, then all `b` values, then all included angles. Each sampled array is cast to `float32` before the remaining parameters are computed. This ordering and casting are relevant when reproducing the supplied dataset.

The uniform distributions apply to these independent inputs, not to all derived parameters or triangle shapes.

## Geometric Relations

The third side follows the cosine law:

$$
c = \sqrt{a^2 + b^2 - 2ab\cos(\theta_{ab})}.
$$

The angle opposite `b` is obtained from:

$$
\theta_b = \arccos\left(\frac{a^2 + c^2 - b^2}{2ac}\right).
$$

The remaining angle follows the angle-sum relation:

$$
\theta_c = \pi - \theta_{ab} - \theta_b.
$$

The code retains the original numerical details: the square-root argument is bounded below by `1e-8`, the denominator used to compute `theta_b` includes `1e-8`, and the argument of `arccos` is clipped to `[-1, 1]`. These details are part of the implementation; they do not define an additional dataset transformation.

## Stored Files

### NPZ

`triangle_clean_seed42_n10000.npz` contains:

- `clean`: a `(10000, 6)` `float32` array in the documented parameter order.
- `seed`: scalar integer 42.
- `samples`: scalar integer 10000.

The name `clean` is the original array key. The supplied NPZ is preserved from the original cached dataset without alteration.

### CSV

The CSV header is:

```text
sample_index,a,b,theta_ab,theta_b,c,theta_c
```

Rows retain the original NPZ order. Values are exported using 17 significant digits, so conversion back to `float32` preserves the original parameter values. The additional index does not carry a class label or a data-partition assignment.

### Metadata

`metadata.json` records the sample count, seed, stored type, parameter order, sampling bounds, units, and derivation rules. `data_dictionary.csv` provides the field definitions in a tabular format.

## Reproduction and Scope

Reproduction was checked with Python 3.11 and NumPy 1.26.4 by comparing the generated parameter array directly with the supplied NPZ. CSV values were also compared after loading as `float32`.

The dataset contains complete synthetic triangles. No filtering, scaling, missing-node masks, train/validation/test split, perturbation scenarios, model outputs, or evaluation results are distributed in this repository. Users can define those operations separately for their own applications.
