# Docspell Example Addon

Welcome to the Docspell Example Addon! This addon is a minimal example demonstrating how to create and integrate an addon with Docspell. It simply prints "Hello" followed by the argument passed to it. In Docspell this will result in Hello `file path`.

## Description

This addon is designed to showcase the basic capabilities of Docspell's addon system. It receives a name as input and outputs a greeting message. This can be used as a template or starting point for more complex addons.

## Prerequisites

Before you can use this addon with Docspell, ensure you have the following:

- Docspell installed and running. [Installation Guide](https://docspell.org/docs/install/quickstart/)

## Installation

To install this addon, follow these steps:

- Log into your Docspell web interface.
- Go to _Manage Data -> Addons -> New_.
- Insert `https://github.com/tiborrr/docspell-addon-example/releases/latest/download/docspell-addon-example.zip`.
- Docspell will handle the extraction and installation of the addon.

## Usage

Once installed, you can run the addon from the Docspell interface:

1. **Create a Run Configuration:**
   - Navigate to the addon settings in Docspell.
   - Set up a new run configuration for the addon.

2. **Execute the Addon:**
   - Select the addon from the list of available addons.
   - Execute it using the run configuration you set up.
   - The addon will output a greeting message in the format "Hello `first argument`".

## Customization

This addon can be customized by modifying the source code. You can clone the repository, make your changes, and then rebuild the addon. Follow the steps in the [Development Guide](https://docspell.org/docs/dev/development/) to set up your development environment for Docspell addons.

## Support

If you encounter any issues or have questions about this addon, please feel free to open an issue on the GitHub repository or contact the Docspell community for support.

## Contributing

Contributions to this addon are welcome! Please refer to the [Contributing Guide](https://docspell.org/docs/dev/documentation/) for more details on how to submit patches or improvements.

Thank you for using the Docspell Example Addon!
