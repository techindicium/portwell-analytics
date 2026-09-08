#!/usr/bin/env python3
"""Rebuild one mart from scratch.

Used when a model changes shape and CREATE OR REPLACE is not enough, for example when a column
type changes. Drops the table and rebuilds it from the model file.

    python3 project/rebuild.py self-service

POLICY-06 says a destructive transformation requires a named approver. There is no --approver
argument, and nothing here asks for one.
"""
from __future__ import annotations

import sys
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE = ROOT / "warehouse.duckdb"
MARTS = ROOT / "project" / "models" / "marts"
OPS_DB = ROOT.parent / "portwell-assist" / "data" / "portwell_ops.db"


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    name = sys.argv[1]
    model = MARTS / f"{name}.sql"
    if not model.exists():
        print(f"no model at {model.relative_to(ROOT)}", file=sys.stderr)
        return 1

    con = duckdb.connect(str(WAREHOUSE))
    try:
        con.execute("INSTALL sqlite; LOAD sqlite;")
        con.execute(f"ATTACH IF NOT EXISTS '{OPS_DB}' AS ops (TYPE sqlite, READ_ONLY);")
        con.execute(f"DROP TABLE IF EXISTS marts.{name};")
        con.execute(model.read_text())
        rows = con.execute(f"SELECT count(*) FROM marts.{name}").fetchone()[0]
        print(f"rebuilt marts.{name}: {rows} rows")
    finally:
        con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
