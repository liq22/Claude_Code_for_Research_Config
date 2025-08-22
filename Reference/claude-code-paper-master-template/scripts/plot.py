"""
Minimal plotting entry. Usage:
  python scripts/plot.py --fn demo --input data/demo.csv --out plots/fig-demo.pdf
"""
import argparse, pathlib
import pandas as pd
import matplotlib.pyplot as plt


def demo(df, out):
    plt.figure()
    for col in df.columns[1:]:
        plt.plot(df[df.columns[0]], df[col], label=col)
    plt.xlabel(df.columns[0])
    plt.ylabel("metric")
    plt.legend()
    pathlib.Path(out).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out, bbox_inches="tight")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fn", required=True)
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    df = pd.read_csv(args.input)
    globals()[args.fn](df, args.out)
