from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Tool:
    name: str
    install_hint: str


RUFF = Tool(name="ruff", install_hint="pip install -r requirements-dev.txt")
PYTEST = Tool(name="pytest", install_hint="pip install -r requirements-dev.txt")
PRECOMMIT = Tool(name="pre-commit", install_hint="pip install -r requirements-dev.txt")


def _require(tool: Tool) -> str:
    path = shutil.which(tool.name)
    if not path:
        raise SystemExit(f"Missing '{tool.name}'. Install dev deps: {tool.install_hint}")
    return path


def _run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, check=False)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)


def _python_manage(*args: str) -> list[str]:
    return [sys.executable, "manage.py", *args]


def cmd_runserver(_: argparse.Namespace) -> None:
    _run(_python_manage("runserver"))


def cmd_migrate(_: argparse.Namespace) -> None:
    _run(_python_manage("migrate"))


def cmd_createsuperuser(_: argparse.Namespace) -> None:
    _run(_python_manage("createsuperuser"))


def cmd_demo(_: argparse.Namespace) -> None:
    _run(_python_manage("seed_demo"))


def cmd_lint(_: argparse.Namespace) -> None:
    ruff = _require(RUFF)
    _run([ruff, "format", "--check", "."])
    _run([ruff, "check", "."])


def cmd_format(_: argparse.Namespace) -> None:
    ruff = _require(RUFF)
    _run([ruff, "format", "."])
    _run([ruff, "check", "--fix", "."])


def cmd_test(args: argparse.Namespace) -> None:
    pytest = _require(PYTEST)
    cmd = [pytest, "-q"]
    if args.cov:
        cmd += [
            "--cov=accounts",
            "--cov=exams",
            "--cov=exam_portal",
            "--cov-report=term-missing",
            "--cov-fail-under=55",
        ]
    _run(cmd)


def cmd_precommit(args: argparse.Namespace) -> None:
    precommit = _require(PRECOMMIT)
    if args.install:
        _run([precommit, "install"])
        return
    _run([precommit, "run", "--all-files"])


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="python scripts/tasks.py",
        description="Cross-platform developer tasks for ExamPortal.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("runserver", help="Run Django dev server")
    p.set_defaults(func=cmd_runserver)

    p = sub.add_parser("migrate", help="Apply DB migrations")
    p.set_defaults(func=cmd_migrate)

    p = sub.add_parser("createsuperuser", help="Create admin user")
    p.set_defaults(func=cmd_createsuperuser)

    p = sub.add_parser("demo", help="Seed demo data")
    p.set_defaults(func=cmd_demo)

    p = sub.add_parser("lint", help="Check formatting and lint")
    p.set_defaults(func=cmd_lint)

    p = sub.add_parser("format", help="Auto-format and auto-fix")
    p.set_defaults(func=cmd_format)

    p = sub.add_parser("test", help="Run tests")
    p.add_argument("--cov", action="store_true", help="Enable coverage and minimum threshold")
    p.set_defaults(func=cmd_test)

    p = sub.add_parser("precommit", help="Run or install pre-commit hooks")
    p.add_argument("--install", action="store_true", help="Install git hooks")
    p.set_defaults(func=cmd_precommit)

    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
