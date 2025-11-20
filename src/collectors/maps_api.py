"""
src/collectors/maps_api.py

Google Maps Distance Matrix collector.

Designed for beginners:
- simple class
- clear methods
- can be reused in future pipelines
"""

import os
import json
from typing import Tuple, Optional, Dict, Any, List

import requests
from dotenv import load_dotenv

from .config_loader import (
    load_config,
    get_google_maps_config,
    get_default_timeout,
    get_raw_output_path,
)


class MapsAPICollector(object):
    """
    Collector for Google Maps Distance Matrix API.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Parameters
        ----------
        config : dict or None
            If None, config.yaml is loaded automatically.
        """
        # Load .env so environment variables are available
        load_dotenv()

        # Load full config if not passed in
        if config is None:
            config = load_config()

        self.config = config

        # Google Maps section from YAML
        gm_cfg = get_google_maps_config(config)

        # Base URL (e.g., https://maps.googleapis.com/maps/api)
        self.base_url = gm_cfg.get("base_url", "").rstrip("/")

        # Endpoint configuration for distance matrix
        endpoints = gm_cfg.get("endpoints", {})
        self.distance_cfg = endpoints.get("distance_matrix", {})

        # Path like "/distancematrix/json"
        self.path = self.distance_cfg.get("path", "")

        # Fixed params from YAML (units, mode, etc.)
        params_cfg = self.distance_cfg.get("params", {})
        self.fixed_params = params_cfg.get("fixed", {})

        # Timeout for HTTP requests
        self.timeout = get_default_timeout(config)

        # Auth setup
        auth_cfg = gm_cfg.get("auth", {})
        env_var_name = auth_cfg.get("api_key_env")

        if not env_var_name:
            raise ValueError(
                "No 'api_key_env' found under 'apis.google_maps.auth' in config.yaml"
            )

        # Actual API key value from environment
        self.api_key = os.getenv(env_var_name)
        if not self.api_key:
            raise ValueError(
                "Environment variable '{}' is not set.\n"
                "Make sure your .env file has:\n"
                "{}=YOUR_REAL_API_KEY_HERE".format(env_var_name, env_var_name)
            )

        # Output file name for raw responses
        output_cfg = self.distance_cfg.get("output", {})
        self.output_file_name = output_cfg.get(
            "file_name", "google_maps_distance_matrix.jsonl"
        )

    # ----------------- Helpers ----------------- #

    def _build_params(self, origin: str, destination: str) -> Dict[str, Any]:
        """
        Build query parameters for Distance Matrix API.
        """
        params = dict(self.fixed_params)  # copy fixed params
        params["origins"] = origin
        params["destinations"] = destination
        params["key"] = self.api_key
        return params

    def fetch_distance_matrix(self, origin: str, destination: str) -> Dict[str, Any]:
        """
        Make the HTTP GET request to Google Maps.
        """
        url = "{}{}".format(self.base_url, self.path)
        params = self._build_params(origin, destination)

        response = requests.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()  # raise error if status != 200

        return response.json()

    def parse_distance_and_duration(
        self, api_response: Dict[str, Any]
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract distance and duration from API response.
        Returns (distance_text, duration_text) or (None, None).
        """
        try:
            element = api_response["rows"][0]["elements"][0]
            distance_text = element["distance"]["text"]
            duration_text = element["duration"]["text"]
            return distance_text, duration_text
        except Exception:
            return None, None

    def save_raw_response(self, api_response: Dict[str, Any]) -> None:
        """
        Append the raw response as a JSON line into a .jsonl file.
        """
        output_path = get_raw_output_path(self.config, self.output_file_name)

        with open(output_path, "a", encoding="utf-8") as f:
            json_line = json.dumps(api_response)
            f.write(json_line + "\n")

    # ----------------- Pipeline-style methods ----------------- #

    def run_for_one_pair(
        self, origin: str, destination: str, save_raw: bool = True
    ) -> Dict[str, Any]:
        """
        Pipeline for a single origin–destination pair.

        Returns
        -------
        dict with:
        - origin
        - destination
        - distance_text
        - duration_text
        - raw (full json response)
        """
        api_response = self.fetch_distance_matrix(origin, destination)
        distance_text, duration_text = self.parse_distance_and_duration(api_response)

        if save_raw:
            self.save_raw_response(api_response)

        return {
            "origin": origin,
            "destination": destination,
            "distance_text": distance_text,
            "duration_text": duration_text,
            "raw": api_response,
        }

    def run_batch(
        self,
        origin_destination_pairs: List[tuple],
        save_raw: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Run the pipeline for many origin–destination pairs.
        """
        results = []
        for origin, destination in origin_destination_pairs:
            result = self.run_for_one_pair(origin, destination, save_raw=save_raw)
            results.append(result)
        return results


# Quick test when running this file directly
if __name__ == "__main__":
    collector = MapsAPICollector()

    origin = "37.7749,-122.4194"       # San Francisco
    destination = "37.8044,-122.2711"  # Oakland

    result = collector.run_for_one_pair(origin, destination, save_raw=False)

    print("Origin      :", result["origin"])
    print("Destination :", result["destination"])
    print("Distance    :", result["distance_text"])
    print("Duration    :", result["duration_text"])