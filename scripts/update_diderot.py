#!/usr/bin/env python3
"""Insert or update the MMALS symplectic concept in a Diderot repository.

The script supports two common layouts:
  1. data/concepts.json containing a JSON list
  2. concepts/<id>.json containing one entry per file

It never deletes unrelated entries and writes a timestamped backup before
modifying an aggregate concepts.json file.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def update_aggregate(target: Path, entry: dict[str, Any]) -> str:
    payload = load_json(target)
    if not isinstance(payload, list):
        raise SystemExit(f"Expected a JSON list in {target}")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = target.with_suffix(target.suffix + f".{stamp}.bak")
    shutil.copy2(target, backup)
    replaced = False
    for index, current in enumerate(payload):
        if isinstance(current, dict) and current.get("id") == entry["id"]:
            payload[index] = entry
            replaced = True
            break
    if not replaced:
        payload.append(entry)
    write_json(target, payload)
    return f"{'Updated' if replaced else 'Added'} {entry['id']} in {target}; backup: {backup}"


def update_file_layout(concepts_dir: Path, entry: dict[str, Any]) -> str:
    target = concepts_dir / f"{entry['id']}.json"
    existed = target.exists()
    if existed:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        shutil.copy2(target, target.with_suffix(target.suffix + f".{stamp}.bak"))
    write_json(target, entry)
    return f"{'Updated' if existed else 'Added'} {target}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("diderot_repo", type=Path, help="Path to mmals-ml-wiki / Diderot repository")
    parser.add_argument("--entry", type=Path, default=Path(__file__).resolve().parents[1] / "diderot" / "entry.json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo = args.diderot_repo.resolve()
    entry = load_json(args.entry.resolve())
    if not isinstance(entry, dict) or not entry.get("id"):
        raise SystemExit("Entry must be a JSON object with an id")

    aggregate_candidates = [repo / "data" / "concepts.json", repo / "assets" / "data" / "concepts.json"]
    aggregate = next((p for p in aggregate_candidates if p.exists()), None)
    concepts_dir = repo / "concepts"

    if args.dry_run:
        if aggregate:
            print(f"Would insert/update {entry['id']} in {aggregate}")
        else:
            print(f"Would write {concepts_dir / (entry['id'] + '.json')}")
        return 0

    if aggregate:
        print(update_aggregate(aggregate, entry))
    else:
        print(update_file_layout(concepts_dir, entry))
    return 0


if __name__ == "__main__":
    sys.exit(main())
