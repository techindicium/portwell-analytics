#!/usr/bin/env python3
"""Build the warehouse.

Attaches the operational database read-only, runs the staging models, then the marts, then the
tests. Order is by directory: staging before marts. Within a directory, filename order.

    python3 project/run.py              # build everything, then run tests
    python3 project/run.py --no-tests   # build only
    python3 project/run.py --tests-only # run tests against whatever is already built

The warehouse file is a build artifact and is not committed.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE = ROOT / "warehouse.duckdb"
OPS_DB = ROOT.parent / "portwell-assist" / "data" / "portwell_ops.db"
MODELS = ROOT / "project" / "models"
TESTS = ROOT / "project" / "tests"


def attach_ops(con: duckdb.DuckDBPyConnection) -> None:
    """Attach the operational database read-only.

    Read-only is not a convention here. DuckDB refuses a write against `ops`, so the extract
    boundary holds even when a model gets it wrong.
    """
    if not OPS_DB.exists():
        raise SystemExit(
            f"{OPS_DB} does not exist.\n"
            f"Build it first: cd {OPS_DB.parents[1]} && python3 scripts/build_db.py"
        )
    con.execute("INSTALL sqlite; LOAD sqlite;")
    con.execute(f"ATTACH '{OPS_DB}' AS ops (TYPE sqlite, READ_ONLY);")


def run_models(con: duckdb.DuckDBPyConnection) -> None:
    con.execute("CREATE SCHEMA IF NOT EXISTS staging;")
    con.execute("CREATE SCHEMA IF NOT EXISTS marts;")
    for stage in ("staging", "marts"):
        for path in sorted((MODELS / stage).glob("*.sql")):
            con.execute(path.read_text())
            print(f"  built {path.relative_to(ROOT)}")


def run_tests(con: duckdb.DuckDBPyConnection) -> int:
    """Every test is a query that must return zero rows. A returned row is a failure."""
    failures = 0
    for path in sorted(TESTS.glob("*.sql")):
        rows = con.execute(path.read_text()).fetchall()
        if rows:
            failures += 1
            print(f"  FAIL {path.name}: {len(rows)} offending row(s), first: {rows[0]}")
        else:
            print(f"  pass {path.name}")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-tests", action="store_true")
    ap.add_argument("--tests-only", action="store_true")
    args = ap.parse_args()

    con = duckdb.connect(str(WAREHOUSE))
    try:
        attach_ops(con)
        if not args.tests_only:
            print(f"Building {WAREHOUSE.name}")
            run_models(con)
        print("Tests")
        failures = 0 if args.no_tests else run_tests(con)
        if not args.no_tests:
            print(f"\n{'FAILED' if failures else 'OK'}: {failures} failing test(s)")
        return 1 if failures else 0
    finally:
        con.close()


if __name__ == "__main__":
    sys.exit(main())
