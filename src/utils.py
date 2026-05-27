"""Shared utilities: config loading, HTTP helpers, path constants."""

from __future__ import annotations

import os
import pathlib
import time

import requests
import yaml
from tenacity import retry, stop_after_attempt, wait_exponential

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
DATA_SUMMARIES = ROOT / "data" / "summaries"
CONFIG_PATH = ROOT / "config" / "docket.yaml"
ENV_PATH = ROOT / ".env"


def _parse_env_file(path: pathlib.Path) -> None:
    """Parse a shell-style env file, handling `export KEY=VALUE` and `. /other/file`."""
    if not path.exists():
        return

    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        # Shell source directive: `. /path/to/file` or `source /path/to/file`
        if line.startswith(". ") or line.startswith("source "):
            sourced = line.split(None, 1)[1].strip()
            _parse_env_file(pathlib.Path(os.path.expanduser(sourced)))
            continue

        if "=" not in line:
            continue

        # Strip optional leading `export `
        if line.startswith("export "):
            line = line[len("export "):]

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key or key in os.environ:
            continue

        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]

        os.environ[key] = value


def load_dotenv_if_present() -> None:
    _parse_env_file(ENV_PATH)


load_dotenv_if_present()


def load_config() -> dict:
    with CONFIG_PATH.open() as fh:
        return yaml.safe_load(fh)


def get_api_key() -> str:
    return os.environ.get("REGULATIONS_GOV_API_KEY", "DEMO_KEY")


def ensure_dirs() -> None:
    for d in (DATA_RAW, DATA_PROCESSED, DATA_SUMMARIES):
        d.mkdir(parents=True, exist_ok=True)


def make_session() -> requests.Session:
    session = requests.Session()
    session.headers["User-Agent"] = "eac-audit-standards/0.1 (research pipeline)"
    return session


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=2, min=4, max=60))
def get_json(
    url: str,
    params: dict | None = None,
    session: requests.Session | None = None,
) -> dict:
    sess = session or make_session()
    resp = sess.get(url, params=params, timeout=30)
    if resp.status_code == 429:
        retry_after = int(resp.headers.get("Retry-After", 30))
        import logging
        logging.getLogger(__name__).warning("Rate limited; sleeping %ds", retry_after)
        time.sleep(retry_after)
        resp.raise_for_status()  # trigger retry
    resp.raise_for_status()
    return resp.json()
