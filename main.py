from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def load_json_file(path: str | None) -> dict | list | None:
    if not path or not Path(path).is_file():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_user_input(path: str) -> dict | None:
    if not path:
        return None
    resolved = Path(path)
    if not resolved.is_absolute():
        resolved = Path.cwd() / resolved
    if not resolved.is_file():
        return None
    with open(resolved, encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return None
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return content


def collect_addon_context() -> dict:
    """Gather all data Docspell provides to an addon."""
    user_input_path = sys.argv[1] if len(sys.argv) > 1 else ""

    return {
        # Argument: file path to user-supplied data from web UI
        "user_input_file": user_input_path,
        "user_input": load_user_input(user_input_path),
        # Basic environment (always provided)
        "addon_dir": os.environ.get("ADDON_DIR"),
        "tmp_dir": os.environ.get("TMP_DIR") or os.environ.get("TMPDIR"),
        "output_dir": os.environ.get("OUTPUT_DIR"),
        "cache_dir": os.environ.get("CACHE_DIR"),
        # Item context (final-process-item, final-reprocess-item, existing-item)
        "item_dir": os.environ.get("ITEM_DIR"),
        "item_data": load_json_file(os.environ.get("ITEM_DATA_JSON")),
        "item_args": load_json_file(os.environ.get("ITEM_ARGS_JSON")),
        "item_original_json": load_json_file(os.environ.get("ITEM_ORIGINAL_JSON")),
        "item_pdf_json": load_json_file(os.environ.get("ITEM_PDF_JSON")),
        "item_original_dir": os.environ.get("ITEM_ORIGINAL_DIR"),
        "item_pdf_dir": os.environ.get("ITEM_PDF_DIR"),
        # Session for dsc (when addon runs on behalf of user)
        "dsc_docspell_url": os.environ.get("DSC_DOCSPELL_URL"),
        "dsc_session": "***" if os.environ.get("DSC_SESSION") else None,
    }


def _log(msg: str) -> None:
    print(msg, file=sys.stderr)


def log_context(ctx: dict) -> None:
    """Log all available context to stderr for debugging."""
    _log("=== Docspell addon context ===")
    _log(f"User input file: {ctx['user_input_file']}")
    _log(f"User input: {ctx['user_input']}")

    _log("\n--- Basic environment ---")
    _log(f"ADDON_DIR: {ctx['addon_dir']}")
    _log(f"TMP_DIR: {ctx['tmp_dir']}")
    _log(f"OUTPUT_DIR: {ctx['output_dir']}")
    _log(f"CACHE_DIR: {ctx['cache_dir']}")

    _log("\n--- Item context ---")
    _log(f"ITEM_DIR: {ctx['item_dir']}")
    if ctx["item_data"]:
        item = ctx["item_data"]
        _log(f"Item: id={item.get('id')}, name={item.get('name')}, collective={item.get('collective')}")
        _log(f"  tags: {item.get('tags', [])}")
        _log(f"  assumedTags: {item.get('assumedTags', [])}")
        _log(f"  attachments: {len(item.get('attachments', []))}")
        if item.get("assumedCorrOrg"):
            _log(f"  assumedCorrOrg: {item['assumedCorrOrg'].get('name')}")
        if item.get("assumedCorrPerson"):
            _log(f"  assumedCorrPerson: {item['assumedCorrPerson'].get('name')}")
        if item.get("assumedConcPerson"):
            _log(f"  assumedConcPerson: {item['assumedConcPerson'].get('name')}")
        if item.get("assumedConcEquip"):
            _log(f"  assumedConcEquip: {item['assumedConcEquip'].get('name')}")
    else:
        _log("Item data: (not available)")
    if ctx["item_args"]:
        _log(f"Item args (upload): {json.dumps(ctx['item_args'], indent=2)}")
    originals = ctx["item_original_json"] or []
    _log(f"ITEM_ORIGINAL_JSON: {len(originals)} files")
    for f in originals:
        _log(f"  - {f.get('name')} (id={f.get('id')}, mimetype={f.get('mimetype')})")
    pdfs = ctx["item_pdf_json"] or []
    _log(f"ITEM_PDF_JSON: {len(pdfs)} files")
    for f in pdfs:
        _log(f"  - {f.get('name')} (id={f.get('id')}, mimetype={f.get('mimetype')})")
    _log(f"ITEM_ORIGINAL_DIR: {ctx['item_original_dir']}")
    _log(f"ITEM_PDF_DIR: {ctx['item_pdf_dir']}")

    _log("\n--- dsc session (when configured) ---")
    _log(f"DSC_DOCSPELL_URL: {ctx['dsc_docspell_url']}")
    _log(f"DSC_SESSION: {ctx['dsc_session']}")


def main() -> None:
    ctx = collect_addon_context()
    log_context(ctx)

    # Return JSON instructions to stdout (empty = no changes)
    # With collectOutput: true, Docspell parses this as addon commands
    print(json.dumps({}))


if __name__ == "__main__":
    main()
