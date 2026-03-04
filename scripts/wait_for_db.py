import os
import sys
import time

import pymysql


def main() -> int:
    host = os.environ.get("DB_HOST", "127.0.0.1")
    port = int(os.environ.get("DB_PORT", "3306"))
    user = os.environ.get("DB_USER", "exam_portal_user")
    password = os.environ.get("DB_PASSWORD", "change_this_password")
    database = os.environ.get("DB_NAME", "exam_portal_db")

    wait_seconds = int(os.environ.get("DB_WAIT_SECONDS", "60"))
    deadline = time.time() + wait_seconds

    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            conn = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                connect_timeout=3,
                read_timeout=3,
                write_timeout=3,
            )
            conn.close()
            return 0
        except Exception as exc:
            last_error = exc
            time.sleep(2)

    print(f"Database not ready after {wait_seconds}s: {last_error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
