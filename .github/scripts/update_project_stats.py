#!/usr/bin/env python3
"""Update README project stars and forks using the GitHub REST API."""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

README_PATH = Path("README.md")

REPOSITORIES = (
    "Yoddikko/kasetPlus",
    "Yoddikko/terminal_portfolio",
    "Yoddikko/GulliverWeb",
    "Yoddikko/yoddChatGPT",
    "Yoddikko/TokenMaxxxxing-Claude