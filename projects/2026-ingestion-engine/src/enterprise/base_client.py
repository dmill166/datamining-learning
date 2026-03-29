"""
BaseAPIClient — The Enterprise Abstraction

Instead of hard-coding the `requests.get()` logic for every single API,
this Base Client reads rules from `config.yaml` to dynamically construct
headers, query parameters, auth injections, and pagination loops.
"""

import os
import requests
from src.logger import get_logger

logger = get_logger(__name__)


class RestAPIClient:
    """A generic, configuration-driven REST client."""
    
    def __init__(self, config: dict):
        self.config = config
        self.name = config["name"]
        self.endpoint = config["endpoint"]
        self.req_def = config.get("request", {})
        self.auth = config.get("auth", {})
        self.pagination = config.get("pagination", {})
        
    def _build_params(self) -> dict:
        """Inject API keys dynamically into query params if required."""
        params = self.req_def.get("params", {}).copy()
        
        if self.auth.get("type") == "query_param":
            token = os.getenv(self.auth.get("env_key"))
            if token:
                params[self.auth.get("param_name")] = token
                
        return params

    def _build_headers(self) -> dict:
        """Inject credentials dynamically into headers if required."""
        headers = self.req_def.get("headers", {}).copy()
        
        if self.auth.get("type") == "headers":
            for header_k, env_k in self.auth.get("env_keys", {}).items():
                val = os.getenv(env_k)
                if val:
                    headers[header_k] = val
                    
        return headers

    def fetch(self) -> list[dict]:
        """Executes the API call based on the declarative pagination strategy."""
        pag_type = self.pagination.get("type", "none")
        
        if pag_type == "none":
            return self._fetch_single()
        elif pag_type == "next_link":
            return self._fetch_paginated()
        else:
            raise NotImplementedError(f"Pagination type '{pag_type}' not supported.")

    def _fetch_single(self) -> list[dict]:
        """Standard single-page REST execution."""
        logger.info(f"[{self.name}] Executing GET {self.endpoint}")
        
        resp = requests.request(
            method=self.req_def.get("method", "GET"),
            url=self.endpoint,
            headers=self._build_headers(),
            params=self._build_params()
        )
        resp.raise_for_status()
        
        # Census HPS returns 2D arrays natively. Base clients often
        # just return the raw payload and let downstream normalize it,
        # but for simplicity we'll just return the JSON object directly.
        return resp.json()

    def _fetch_paginated(self) -> list[dict]:
        """Executes cursor-based or next-link pagination loops dynamically."""
        results = []
        url = self.endpoint
        
        res_key = self.pagination["results_key"]
        next_key = self.pagination["next_url_key"]
        
        page_num = 1
        while url:
            logger.info(f"[{self.name}] Fetching page {page_num}...")
            resp = requests.get(
                url, 
                headers=self._build_headers(), 
                params=self._build_params() if page_num == 1 else None
            )
            resp.raise_for_status()
            payload = resp.json()
            
            page_data = payload.get(res_key, [])
            results.extend(page_data)
            
            url = payload.get(next_key)
            page_num += 1
            
        return results
