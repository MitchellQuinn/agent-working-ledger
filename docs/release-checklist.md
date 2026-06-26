# Release Checklist

This checklist is for validating and publishing the public alpha `v0.1.0`
source release. It is not a PyPI publication checklist.

## v0.1.0 Checks

- [ ] Confirm `pyproject.toml` contains `version = "0.1.0"`.
- [ ] Confirm `agent_working_ledger/__init__.py` reports `__version__ = "0.1.0"`.
- [ ] Confirm `CHANGELOG.md` has a `0.1.0` entry with release notes.
- [ ] Run the test suite.

  ```bash
  python -m pip install -U build pytest
  python -m pytest
  python -m unittest discover -s tests
  ```

- [ ] Run the compile check used by CI.

  ```bash
  python -m compileall -q agent_working_ledger tests
  ```

- [ ] Build the wheel and sdist.

  ```bash
  python -m build
  ```

- [ ] Inspect the wheel and sdist contents.

  ```bash
  python -m zipfile -l dist/agent_working_ledger-0.1.0-py3-none-any.whl
  python -m tarfile -l dist/agent_working_ledger-0.1.0.tar.gz
  ```

- [ ] Install from the built wheel in a clean environment.

  ```bash
  python -m venv .venv-release-smoke
  . .venv-release-smoke/bin/activate
  python -m pip install --force-reinstall dist/agent_working_ledger-0.1.0-py3-none-any.whl
  ```

  On Windows PowerShell, activate with:

  ```powershell
  .venv-release-smoke\Scripts\Activate.ps1
  ```

- [ ] Smoke-test the installed CLI.

  ```bash
  awl --help
  awl --version
  awl assets
  awl new "Release smoke" --root release-smoke-ledgers --owner-id release-smoke --handoff --machine-state
  awl check release-smoke-ledgers/release-smoke
  awl summarize release-smoke-ledgers/release-smoke
  ```

- [ ] Remove local smoke-test output.

  ```bash
  rm -rf release-smoke-ledgers .venv-release-smoke
  ```

## Manual GitHub Release Steps

- [ ] Create the git tag.

  ```bash
  git tag -a v0.1.0 -m "Agent Working Ledger v0.1.0"
  ```

- [ ] Push the tag.

  ```bash
  git push origin v0.1.0
  ```

- [ ] Create a GitHub Release for `v0.1.0` using the `CHANGELOG.md` notes.
- [ ] Verify the README source-install command still pins the intended release
  tag.
- [ ] Do not claim PyPI availability unless a separate PyPI publication has
  actually been completed and verified.
