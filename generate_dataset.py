from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np


PARAM_NAMES = ["a", "b", "theta_ab", "theta_b", "c", "theta_c"]


def generate_triangle_dataset(n_samples: int = 10000, seed: int = 42) -> np.ndarray:
    """Return complete triangle parameters in the documented column order."""
    rng = np.random.default_rng(seed)
    a = rng.uniform(0.5, 5.0, size=n_samples).astype(np.float32)
    b = rng.uniform(0.5, 5.0, size=n_samples).astype(np.float32)
    theta_ab = rng.uniform(math.pi / 6, 5 * math.pi / 6, size=n_samples).astype(np.float32)
    c_sq = a**2 + b**2 - 2.0 * a * b * np.cos(theta_ab)
    c = np.sqrt(np.maximum(c_sq, 1e-8)).astype(np.float32)
    cos_theta_b = (a**2 + c**2 - b**2) / (2.0 * a * c + 1e-8)
    theta_b = np.arccos(np.clip(cos_theta_b, -1.0, 1.0)).astype(np.float32)
    theta_c = (math.pi - theta_ab - theta_b).astype(np.float32)
    return np.stack([a, b, theta_ab, theta_b, c, theta_c], axis=1).astype(np.float32)


def export_dataset(clean: np.ndarray, seed: int, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"triangle_clean_seed{seed}_n{len(clean)}"
    np.savez_compressed(output_dir / f"{stem}.npz", clean=clean, seed=np.array(seed), samples=np.array(len(clean)))
    with (output_dir / f"{stem}.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["sample_index", *PARAM_NAMES])
        for index, row in enumerate(clean):
            writer.writerow([index, *[format(float(value), ".17g") for value in row]])
    metadata = {
        "dataset_type": "synthetic triangle parameters",
        "samples": len(clean),
        "seed": seed,
        "dtype": str(clean.dtype),
        "npz_array_name": "clean",
        "columns": PARAM_NAMES,
        "sampling": {
            "a": {"distribution": "uniform", "minimum": 0.5, "maximum": 5.0},
            "b": {"distribution": "uniform", "minimum": 0.5, "maximum": 5.0},
            "theta_ab": {"distribution": "uniform", "minimum_radians": math.pi / 6, "maximum_radians": 5 * math.pi / 6},
        },
        "derived_parameters": {
            "c": "sqrt(a^2 + b^2 - 2*a*b*cos(theta_ab))",
            "theta_b": "acos((a^2 + c^2 - b^2)/(2*a*c))",
            "theta_c": "pi - theta_ab - theta_b",
        },
        "units": {"side_lengths": "synthetic length unit", "angles": "radian"},
        "index": "zero-based sample_index in the CSV; original row order preserved",
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Construct a synthetic triangle dataset.")
    parser.add_argument("--samples", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent / "generated_data")
    args = parser.parse_args()
    clean = generate_triangle_dataset(args.samples, args.seed)
    export_dataset(clean, args.seed, args.output_dir)
    print(f"Saved {len(clean)} triangles to {args.output_dir}")


if __name__ == "__main__":
    main()
