"""Single source of truth for addon name and version.

Read from docspell-addon.yml. When creating a release, update only:
  - docspell-addon.yml: meta.version and runner.docker.image
"""

from __future__ import annotations

import re
from pathlib import Path

_ADDON_YML = Path(__file__).parent / "docspell-addon.yml"
_text = _ADDON_YML.read_text()

ADDON_NAME: str = re.search(r'name:\s*["\']([^"\']+)["\']', _text).group(1)
VERSION: str = re.search(r'version:\s*["\']([^"\']+)["\']', _text).group(1)
ADDON_DIR: str = f"addons/{ADDON_NAME}-{VERSION}"
