"""Database migration script. Applies incremental SQL migrations.

Usage: python db/migrate.py
Reads APP_ENV to determine which env file to load (default: dev).
Scans db/migrations/ for {version}_{description}.sql files.
"""

import os
import re
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import psycopg2

from services.config_service import ConfigService

MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"
MIGRATION_PATTERN = re.compile(r"^(\d+)_(.+)\.sql$")


def get_applied_versions(conn):
    """Get set of already-applied migration versions."""
    with conn.cursor() as cur:
        cur.execute("SELECT version FROM schema_migrations ORDER BY version")
        return {row[0] for row in cur.fetchall()}


def get_pending_migrations(applied):
    """Scan migrations dir, return sorted list of unapplied (version, name, path)."""
    if not MIGRATIONS_DIR.exists():
        MIGRATIONS_DIR.mkdir(parents=True, exist_ok=True)
        return []

    pending = []
    for f in sorted(MIGRATIONS_DIR.iterdir()):
        match = MIGRATION_PATTERN.match(f.name)
        if not match:
            continue
        version, name = match.group(1), match.group(2)
        if version not in applied:
            pending.append((version, name, f))
    return pending


def apply_migration(conn, version, name, path):
    """Apply a single migration within a transaction."""
    sql = path.read_text(encoding="utf-8")
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            cur.execute(
                "INSERT INTO schema_migrations (version, name) VALUES (%s, %s)",
                (version, name),
            )
        conn.commit()
        print(f"  Applied: {version}_{name}.sql")
    except Exception as e:
        conn.rollback()
        print(f"  FAILED: {version}_{name}.sql - {str(e)}")
        sys.exit(1)


def main():
    config = ConfigService()
    config.load()

    try:
        conn = psycopg2.connect(config.database_url)
    except Exception as e:
        print(f"Cannot connect to database: {str(e)}")
        sys.exit(1)

    try:
        applied = get_applied_versions(conn)
        pending = get_pending_migrations(applied)

        if not pending:
            print("No pending migrations.")
            return

        print(f"Found {len(pending)} pending migration(s):")
        for version, name, path in pending:
            apply_migration(conn, version, name, path)

        print("All migrations applied.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
