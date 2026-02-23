# Docspell Example Addon

A minimal example addon demonstrating how to create and integrate an addon with Docspell. It showcases all data Docspell provides to addons: user input, environment variables, item data, file metadata, and dsc session.

## Description

This addon is designed to showcase the Docspell addon interface. It reads user input from the file argument, item data from environment variables, and logs everything to stderr for debugging. It returns empty JSON to stdout (no changes applied). Use it as a template or starting point for more complex addons.

## Prerequisites

- Docspell installed and running. [Installation Guide](https://docspell.org/docs/install/quickstart/)

## Installation

1. Log into your Docspell web interface.
2. Go to _Manage Data → Addons → New_.
3. Insert `https://github.com/tiborrr/docspell-addon-example/releases/latest/download/docspell-addon-example.zip`.
4. Docspell will extract and install the addon.

## Usage

1. **Create a Run Configuration:**
   - Navigate to the addon settings in Docspell.
   - Set up a new run configuration for the addon (e.g. trigger: final-process-item).

2. **Execute the Addon:**
   - The addon runs automatically when triggered, or select it to run on an item.
   - Check Docspell logs to see the addon output (it logs all available data to stderr).

## Development

### Running Tests

```bash
python -m pytest test/main_test.py -v
```

### Version Management

The version is defined in `docspell-addon.yml`. When creating a release, update only:

- `meta.version` (e.g. `"1.3.0"`)
- `runner.docker.image` (e.g. `tiborrr/docspell-addon-example:1.3.0`)

The `version.py` module reads from this file so tests and other tooling stay in sync.

## Customization

Clone the repository, modify the source code, and rebuild. See the [Docspell addon documentation](https://docspell.org/docs/addons/writing/) for the full interface.

## Support

Open an issue on the GitHub repository or contact the Docspell community for support.

## Contributing

Contributions are welcome. See the [Docspell contributing guide](https://docspell.org/docs/dev/documentation/) for details.
