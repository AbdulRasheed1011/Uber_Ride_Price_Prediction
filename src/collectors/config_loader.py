"""
src/collectors/config_loader.py

Simple helpers to:
- find project root
- load config.yaml
- get some pieces from config
"""

import yaml
from pathlib import Path
from typing import Optional, Dict, Any


def get_project_root() -> Path:
    """
    Assume this file lives in:
        project_root/src/collectors/config_loader.py

    parents[0] -> .../collectors
    parents[1] -> .../src
    parents[2] -> .../project_root  (Uber)
    """
    return Path(__file__).resolve().parents[2]


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load the YAML config file (config.yaml) as a Python dict.
    """
    if config_path is None:
        project_root = get_project_root()
        cfg_path = project_root / "config.yaml"
    else:
        cfg_path = Path(config_path)

    if not cfg_path.exists():
        raise FileNotFoundError("Config file not found at: {}".format(cfg_path))

    with open(cfg_path, "r") as f:
        config = yaml.safe_load(f)

    return config


def get_google_maps_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get the google_maps section from config.
    """
    try:
        return config["apis"]["google_maps"]
    except KeyError as e:
        raise ValueError(
            "Missing 'apis.google_maps' in config.yaml – check your YAML structure."
        ) from e


def get_default_timeout(config: Dict[str, Any]) -> int:
    """
    Get default timeout (seconds) from config, or 10 if missing.
    """
    return config.get("data_collection", {}).get("default_timeout_seconds", 10)


def get_raw_output_path(config: Dict[str, Any], file_name: str) -> Path:
    """
    Build full path for saving raw API responses.
    Uses:
        storage.raw_data_dir
    """
    project_root = get_project_root()
    storage_cfg = config.get("storage", {})
    raw_dir = storage_cfg.get("raw_data_dir", "data/raw")

    raw_dir_path = project_root / raw_dir
    raw_dir_path.mkdir(parents=True, exist_ok=True)

    return raw_dir_path / file_name