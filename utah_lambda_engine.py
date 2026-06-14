#!/usr/bin/env python3
"""
Utah Lambda Engine - v25.0 Omega-Build
Serverless handler invoke without container image pulls.
"""

import importlib.util
import json
import os
from typing import Any, Callable, Optional

UTAH_DATA_DIR = os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere")
LAMBDA_ROOT = os.path.join(UTAH_DATA_DIR, "lambda")


def _handler_path(fn_name: str) -> str:
    return os.path.join(LAMBDA_ROOT, fn_name, "handler.py")


def register_function(fn_name: str, handler_source: Optional[str] = None) -> str:
    path = os.path.join(LAMBDA_ROOT, fn_name)
    os.makedirs(path, exist_ok=True)
    handler_file = os.path.join(path, "handler.py")
    if handler_source:
        with open(handler_file, "w") as f:
            f.write(handler_source)
    elif not os.path.exists(handler_file):
        with open(handler_file, "w") as f:
            f.write(
                "def handler(event, context):\n"
                "    name = event.get('name', 'World')\n"
                "    return {'message': f'Hello {name} from Utah Lambda!'}\n"
            )
    return handler_file


def load_handler(fn_name: str) -> Callable[[dict, dict], Any]:
    handler_path = _handler_path(fn_name)
    if not os.path.exists(handler_path):
        raise FileNotFoundError(f"Lambda function not found: {fn_name}")
    spec = importlib.util.spec_from_file_location(f"lambda_{fn_name}", handler_path)
    if not spec or not spec.loader:
        raise ImportError(f"Cannot load lambda: {fn_name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.handler


def invoke(fn_name: str, event: dict, context: Optional[dict] = None) -> Any:
    handler_fn = load_handler(fn_name)
    return handler_fn(event, context or {"function": fn_name})
