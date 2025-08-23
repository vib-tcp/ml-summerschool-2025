# Setting up UV

## Table of Contents

1. [What Is UV, and Why Does It Exist?](#1-what-is-uv-and-why-does-it-exist)
2. [Installing UV on Different Platforms](#2-installing-uv-on-different-platforms)
3. [Initializing a Project with `uv init`](#3-initializing-a-project-with-uv-init)
4. [Managing Dependencies: `uv add` & `uv remove`](#4-managing-dependencies-uv-add-and-uv-remove)
5. [Syncing & Locking Environments](#5-syncing-and-locking-environments)
6. [Setting the Python Version](#6-setting-the-python-version-to-311)
7. [Summary](#7-summary-for-students)
8. [Exercise](#8-exercise)

## 1. What Is UV, and Why Does It Exist?

**UV** is a fast, all-in-one Python package manager written in Rust. It merges the capabilities of tools like `pip`, `pip-tools`, `virtualenv`, `pyenv`, `pipx`, `poetry`, and `twine` into a unified, high-performance tool.

For additional information, see official documentation [here](https://docs.astral.sh/uv/).

### It solves key problems such as:

* **Slow installs**: UV is **8–10× faster than pip without cache**, and **80–115× faster with a warm cache**.
* **Environment complexity**: Automatically manages virtual environments, dependencies, lockfiles, and even Python version installation.
* **Reproducibility**: Generates lockfiles (`uv.lock`) for consistent environments across machines.
* **Ease of use**: Combines many separate tools into one simple interface.

---

## 2. Installing UV on Different Platforms

You can install UV in several ways depending on your system:

### Linux/macOS
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
#pip install uv
#pipx install uv
#brew install uv
```

### Windows
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
#pip install uv
#pipx install uv
```

**After installation**, confirm it's working:

```bash
$ uv
An extremely fast Python package manager.

Usage: uv [OPTIONS] <COMMAND>
...
```

---

## 3. Initializing a Project with `uv init`

To create a new Python project scaffold:

```bash
$ uv init hello-world
$ cd hello-world
```

Or, in an existing directory:

```bash
$ mkdir hello-world
$ cd hello-world
$ uv init
```

**This generates**:

* `pyproject.toml`
* `README.md`, `main.py` (with a simple hello-world script)
* `.python-version` (chooses a default Python version)
* `.gitignore`
  A project’s virtual environment (`.venv`) and lockfile (`uv.lock`) are created later upon running or syncing.

---

## 4. Managing Dependencies: `uv add` & `uv remove`

* **Add a dependency**:

  ```bash
  $ uv add requests
  ```

  Optionally specify versions:

  ```bash
  $ uv add 'requests==2.31.0'
  ```

  Or add from Git:

  ```bash
  $ uv add git+https://github.com/psf/requests
  ```

  For `requirements.txt`:

  ```bash
  $ uv add -r requirements.txt -c constraints.txt
  ```

* **Remove a dependency**:

  ```bash
  $ uv remove requests
  ```

These commands update your `pyproject.toml`, the lockfile, and the environment (unless overridden).

---

## 5. Syncing & Locking Environments

* **Lock dependencies**:

  ```bash
  $ uv lock
  ```

* **Sync your environment**:

  ```bash
  $ uv sync
  ```

This ensures your `.venv` matches the lockfile. You can then activate the virtual environment:

* **macOS/Linux**:

  ```bash
  $ source .venv/bin/activate
  ```

* **Windows**:

  ```powershell
  PS> .venv\Scripts\activate
  ```


> Tip from the community:
> “If you clone an existing repo, this environment can be rebuilt with `uv sync`. uv auto‑syncs on commands like `uv run`.”

---

## 6. Setting the Python Version

To pin your project to Python 3.11:

```bash
$ uv python install 3.11
$ uv python pin 3.11
```

This creates or updates `.python-version` accordingly.

You can also use a single command to create a virtual environment with that version:

```bash
$ uv venv --python 3.11
```

---

## 7. Summary for Students

1. **What & Why**: UV is a fast, all-in-one Python project manager that unifies environments, dependencies, scripts, and version management.
2. **Install** via script, Python, pipx, or brew depending on your system.
3. **Initialize** your project using `uv init`.
4. **Add/remove** dependencies easily (`uv add` / `uv remove`).
5. **Lock** and **sync** your environment for reproducibility.
6. **Pin Python version** to 3.11 for consistency.

## 8. Exercise

Create a new project and set up a virtual environment with Python 3.11. Once you create this project add to the project the following dependencies:

```
pandas
numpy
matplotlib
seaborn
```

Once you have added the dependencies, lock and sync your environment.
