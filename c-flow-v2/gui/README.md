# C‑Flow Proof-of-Concept GUI

This small GUI wraps the existing CLI to make common tasks accessible without a terminal. It allows running any `claude-flow` command and viewing the output in a window.

Run `python3 main.py` to launch the GUI. The application automatically locates
the bundled `claude-flow` script relative to the GUI file. You can override the
path via the `CFLOW_CLI_PATH` environment variable or by passing `cli_path` when
instantiating `CFlowGUI`.

Tests are located in `tests/` and provide 100% coverage for the implemented logic.
