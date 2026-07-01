import logging
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from app.config import settings

logger = logging.getLogger(__name__)


def get_backup_dir() -> Path:
    path = Path(settings.BACKUP_DIR)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _parse_db_url():
    url = settings.DATABASE_URL
    parsed = urlparse(url)
    user = parsed.username or "root"
    password = parsed.password or ""
    host = parsed.hostname or "localhost"
    port = parsed.port or 3306
    db_name = parsed.path.lstrip("/") if parsed.path else ""
    return {"user": user, "password": password, "host": host, "port": port, "db": db_name}


def create_backup() -> str:
    db = _parse_db_url()
    backup_dir = get_backup_dir()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"worldplate_backup_{timestamp}.sql"
    filepath = backup_dir / filename

    env = os.environ.copy()
    env.setdefault("MYSQL_PWD", db["password"])

    result = subprocess.run(
        [
            "mysqldump",
            f"--host={db['host']}",
            f"--port={db['port']}",
            f"--user={db['user']}",
            "--routines",
            "--triggers",
            "--single-transaction",
            "--quick",
            db["db"],
        ],
        capture_output=True,
        text=True,
        env=env,
        timeout=120,
    )

    if result.returncode != 0:
        logger.error("Backup failed: %s", result.stderr)
        raise RuntimeError("Backup failed. Check server logs for details.")

    filepath.write_text(result.stdout, encoding="utf-8")
    return str(filepath)


def list_backups() -> list[dict]:
    backup_dir = get_backup_dir()
    files = []
    for f in sorted(backup_dir.glob("worldplate_backup_*.sql"), reverse=True):
        stat = f.stat()
        files.append({
            "filename": f.name,
            "size": stat.st_size,
            "created_at": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
        })
    return files


def delete_backup(filename: str) -> None:
    backup_dir = get_backup_dir()
    filepath = backup_dir / filename
    if filepath.exists():
        filepath.unlink()


def _get_mysql_client():
    db = _parse_db_url()
    return [
        "mysql",
        f"--host={db['host']}",
        f"--port={db['port']}",
        f"--user={db['user']}",
        f"--database={db['db']}",
    ]


def restore_backup(file_path: str) -> None:
    db = _parse_db_url()
    env = os.environ.copy()
    env.setdefault("MYSQL_PWD", db["password"])

    result = subprocess.run(
        _get_mysql_client(),
        stdin=open(file_path, "r", encoding="utf-8"),
        capture_output=True,
        text=True,
        env=env,
        timeout=300,
    )

    if result.returncode != 0:
        logger.error("Restore failed: %s", result.stderr)
        raise RuntimeError("Restore failed. Check server logs for details.")
