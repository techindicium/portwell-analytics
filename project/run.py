#!/usr/bin/env python3
"""Build the warehouse.

Loads the operational extract in data/ops-extract/, runs the staging models, then the marts,
then the tests. Order is by directory: staging before marts, filename order within each.

    python3 project/run.py              # build everything, then run tests
    python3 project/run.py --no-tests   # build only
    python3 project/run.py --tests-only # run tests against whatever is already built
    python3 project/run.py --live       # read the operational database directly instead

The extract is a snapshot somebody took by hand. Its date is in
data/ops-extract/extract-manifest.yaml and nowhere else. Nothing here compares that date to
the period being reported on.

--live attaches the operational database read-only, when the file happens to be reachable on
this machine. It usually is not, which is why the extract exists.

The warehouse file is a build artifact and is not committed.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE = ROOT / "warehouse.duckdb"
OPS_DB = ROOT.parent / "portwell-portal" / "data" / "portwell_ops.db"
MODELS = ROOT / "project" / "models"
TESTS = ROOT / "project" / "tests"
EXTRACT = ROOT / "data" / "ops-extract"


def load_extract(con: duckdb.DuckDBPyConnection) -> None:
    """Expose the committed extract as the `ops` schema.

    The models read `ops.<table>` either way, so switching between the extract and the live
    database changes nothing downstream. What changes is how old the numbers are.
    """
    if not EXTRACT.exists():
        raise SystemExit(f"missing {EXTRACT.relative_to(ROOT)}")
    # Timestamps are text in the operational database, and the models parse them. Pin those
    # columns to VARCHAR so the extract has the same shape the live attach would give.
    text_columns = {
        "ticket": ["opened_at"],
        "interaction": ["occurred_at"],
        "suggestion": ["created_at"],
    }
    con.execute("CREATE SCHEMA IF NOT EXISTS ops;")
    for csv_path in sorted(EXTRACT.glob("*.csv")):
        table = csv_path.stem
        types = ", ".join(f"'{c}': 'VARCHAR'" for c in text_columns.get(table, []))
        options = f", types={{{types}}}" if types else ""
        con.execute(
            f"CREATE OR REPLACE TABLE ops.{table} AS "
            f"SELECT * FROM read_csv_auto('{csv_path}', header=true{options})"
        )
    print(f"  loaded extract from {EXTRACT.relative_to(ROOT)}")


def attach_ops(con: duckdb.DuckDBPyConnection) -> None:
    """Attach the operational database read-only.

    Read-only is not a convention. DuckDB refuses a write against `ops`, so the boundary holds
    even when a model gets it wrong.
    """
    if not OPS_DB.exists():
        raise SystemExit(
            f"{OPS_DB} is not reachable from here.\n"
            f"Drop --live to build from the extract in {EXTRACT.relative_to(ROOT)}."
        )
    # A previous extract build leaves an `ops` schema inside the warehouse, which would collide
    # with the attached database of the same name.
    con.execute("DROP SCHEMA IF EXISTS ops CASCADE;")
    con.execute("INSTALL sqlite; LOAD sqlite;")
    con.execute(f"ATTACH '{OPS_DB}' AS ops (TYPE sqlite, READ_ONLY);")
    print(f"  attached {OPS_DB} read-only")


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
    ap.add_argument("--live", action="store_true", help="read the operational database instead of the extract")
    args = ap.parse_args()

    con = duckdb.connect(str(WAREHOUSE))
    try:
        if args.live:
            attach_ops(con)
        else:
            load_extract(con)
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
