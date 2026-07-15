#!/usr/bin/env python3
"""Update README project and organization stars/forks using GitHub's REST API."""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

README_PATH = Path("README.md")

REPOSITORIES = (
    "Yoddikko/kasetPlus",
    "Yoddikko/terminal_portfolio",
    "Yoddikko/GulliverWeb",