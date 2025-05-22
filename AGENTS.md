# AGENTS.md — Quick Guide

## Dev Environment Tips

A Python 3.12 virtual environment has already been created by the setup script, and should activate automatically for you as the following has been added to `~/.bashrc`:

```bash
. venv/bin/activate
```

If something seems like it's not installed for you, try re-activating the environment.
(You can double check this with the `which python` command.)

*NOTE:* your environment does not have any network access, so don't try to install something or do anything that requires the internet.

## Testing Instructions

All tests live in `sim/tests/`.

Run a test file like so:

  ```bash
  pytest -xvs tests/test_traffic_patterns.py
  ```

## Running the Simulator

```bash
python -m sim           # default four-way, 60 sim-min
```
