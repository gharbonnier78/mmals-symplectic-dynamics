#!/usr/bin/env python3
"""Validate structure, determinism, and executable assertions for the Volovich notebook."""
from __future__ import annotations

import argparse
import importlib.util
import re
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def load_generator(path: Path):
    spec = importlib.util.spec_from_file_location("volovich_generator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import generator: {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def canonical_cells(nb):
    return [(c.cell_type, c.id, c.source) for c in nb.cells]


def output_text(nb):
    chunks = []
    for cell in nb.cells:
        for out in cell.get("outputs", []):
            if out.get("output_type") == "stream":
                chunks.append(out.get("text", ""))
            elif out.get("output_type") in {"execute_result", "display_data"}:
                text = out.get("data", {}).get("text/plain")
                if text:
                    chunks.append(text)
    return "\n".join(chunks)


def metric(text: str, name: str) -> float:
    m = re.search(rf"{re.escape(name)}=([0-9.eE+-]+)", text)
    if not m:
        raise AssertionError(f"missing metric {name}")
    return float(m.group(1))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook", nargs="?", default="01_volovich_realification_falsification.ipynb")
    parser.add_argument("--generator", default="scripts/generate_volovich_notebook.py")
    args = parser.parse_args()

    nb_path = Path(args.notebook)
    gen_path = Path(args.generator)
    nb = nbformat.read(nb_path, as_version=4)
    assert len(nb.cells) == 22, len(nb.cells)
    assert sum(c.cell_type == "code" for c in nb.cells) == 10
    assert all(c.get("id") for c in nb.cells)

    generator = load_generator(gen_path)
    expected = generator.build_notebook()
    assert canonical_cells(nb) == canonical_cells(expected), "notebook differs from deterministic generator"

    executed = NotebookClient(nb, timeout=180, kernel_name="python3", allow_errors=False).execute()
    text = output_text(executed)
    real_err = metric(text, "max_realification_error")
    sym_err = metric(text, "symplectic_residual")
    orth_err = metric(text, "orthogonal_residual")
    assert real_err < 1e-12
    assert sym_err < 1e-12
    assert orth_err < 1e-12
    assert "FALSIFIED" in text and "UNSUPPORTED" in text and "SUPPORTED" in text

    print("validation=PASS")
    print("cells=22 code_cells=10")
    print(f"max_realification_error={real_err:.15e}")
    print(f"symplectic_residual={sym_err:.15e}")
    print(f"orthogonal_residual={orth_err:.15e}")


if __name__ == "__main__":
    main()
