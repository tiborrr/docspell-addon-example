"""Single source of truth for addon name and version.

Read from docspell-addon.yml. When creating a release, update only:
  - docspell-addon.yml: meta.version and runner.docker.image
"""

from __future__ import annotations

import re
from pathlib import Path

_ADDON_YML = Path(__file__).parent / "docspell-addon.yml"
_text = _ADDON_YML.read_text()

_name_match = re.search(r'name:\s*["\']([^"\']+)["\']', _text)
_version_match = re.search(r'version:\s*["\']([^"\']+)["\']', _text)
if _name_match is None or _version_match is None:
    raise ValueError("Could not parse name or version from docspell-addon.yml")
ADDON_NAME: str = _name_match.group(1)
VERSION: str = _version_match.group(1)
ADDON_DIR: str = f"addons/{ADDON_NAME}-{VERSION}"
