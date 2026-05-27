"""Shared utilities: config loading, HTTP helpers, path constants."""

from __future__ import annotations

import os
import pathlib

import requests
import yaml
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
DATA_SUMMARIES = ROOT / "data" / "summaries"
CONFIG_PATH = ROOT / "config" / "docket.yaml"

load_dotenv(ROOT / ".env")


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


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def get_json(
    url: str,
    params: dict | None = None,
    session: requests.Session | None = None,
) -> dict:
    sess = session or make_session()
    resp = sess.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()
