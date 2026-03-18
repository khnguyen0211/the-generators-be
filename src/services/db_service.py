"""DatabaseService - Singleton for PostgreSQL connection management."""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, TYPE_CHECKING

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor

if TYPE_CHECKING:
    from services.config_service import ConfigService
    from services.logger_service import LoggerService

MIGRATIONS_DIR = Path(__file__).resolve().parent.parent.parent / "db" / "migrations"
MIGRATION_PATTERN = re.compile(r"^(\d+)_(.+)\.sql$")


class DatabaseService:
    """Singleton database service with connection pooling."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._pool = None
            cls._instance._available = False
            cls._instance._logger = None
        return cls._instance

    def initialize(self, config: "ConfigService", logger: "LoggerService") -> None:
        """Set up connection pool and verify connectivity."""
        self._logger = logger
        try:
            self._pool = pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                dsn=config.database_url,
            )
            conn = self._pool.getconn()
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                self._available = True
                logger.info(f"Database connected at {config.db_host}:{config.db_port}/{config.db_name}")
            finally:
                self._pool.putconn(conn)
            self._run_migrations()
        except Exception as e:
            self._available = False
            logger.error(f"Database connection failed: {str(e)}")

    @property
    def available(self) -> bool:
        return self._available

    def execute(self, query: str, params: tuple = None) -> int:
        """Execute INSERT/UPDATE/DELETE, return affected row count."""
        if not self._available:
            return 0
        conn = self._pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()
                return cur.rowcount
        except Exception as e:
            conn.rollback()
            raise
        finally:
            self._pool.putconn(conn)

    def fetch_one(self, query: str, params: tuple = None) -> Optional[Dict[str, Any]]:
        """Execute SELECT, return single row as dict or None."""
        if not self._available:
            return None
        conn = self._pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                row = cur.fetchone()
                return dict(row) if row else None
        finally:
            self._pool.putconn(conn)

    def fetch_all(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Execute SELECT, return all rows as list of dicts."""
        if not self._available:
            return []
        conn = self._pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                return [dict(row) for row in cur.fetchall()]
        finally:
            self._pool.putconn(conn)

    def health_check(self) -> dict:
        """Check database connectivity."""
        if not self._available or not self._pool:
            return {"status": "down"}
        try:
            conn = self._pool.getconn()
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                return {"status": "up"}
            finally:
                self._pool.putconn(conn)
        except Exception:
            return {"status": "down"}

    def close(self) -> None:
        """Close all pool connections."""
        if self._pool:
            self._pool.closeall()
            self._available = False
            if self._logger:
                self._logger.info("Database connections closed")

    def _run_migrations(self) -> None:
        """Auto-apply pending migrations on startup."""
        if not MIGRATIONS_DIR.exists():
            MIGRATIONS_DIR.mkdir(parents=True, exist_ok=True)
            return

        conn = self._pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT version FROM schema_migrations ORDER BY version")
                applied = {row[0] for row in cur.fetchall()}

            pending = []
            for f in sorted(MIGRATIONS_DIR.iterdir()):
                match = MIGRATION_PATTERN.match(f.name)
                if not match:
                    continue
                version, name = match.group(1), match.group(2)
                if version not in applied:
                    pending.append((version, name, f))

            if not pending:
                self._logger.info("Database schema is up to date")
                return

            self._logger.info(f"Found {len(pending)} pending migration(s)")
            for version, name, path in pending:
                sql = path.read_text(encoding="utf-8")
                try:
                    with conn.cursor() as cur:
                        cur.execute(sql)
                        cur.execute(
                            "INSERT INTO schema_migrations (version, name) VALUES (%s, %s)",
                            (version, name),
                        )
                    conn.commit()
                    self._logger.info(f"Migration applied: {version}_{name}.sql")
                except Exception as e:
                    conn.rollback()
                    self._logger.error(f"Migration failed: {version}_{name}.sql - {str(e)}")
                    return
        finally:
            self._pool.putconn(conn)
