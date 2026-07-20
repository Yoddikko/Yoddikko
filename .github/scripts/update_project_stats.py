#!/usr/bin/env python3
"""Update README star/fork totals for repositories and public organizations."""

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

README = Path("README.md")

REPOSITORIES = (
    "Yoddikko/kasetPlus",
    "Yoddikko/terminal_portfolio",
    "Yoddikko/GulliverWeb",
    "Yoddikko/y