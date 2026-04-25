# Virtual Environment

Dependencies are managed in a `.venv` virtual environment.

## Setup

```
make install
```

This creates `.venv/` and installs the packages in `requirements.txt` (PyMuPDF, pytest, mcp).

## direnv (optional)

[direnv](https://direnv.net) automatically activates the venv when you `cd` into the project and deactivates it when you leave. A `.envrc` is already checked in.

Install direnv if you haven't:

```
brew install direnv
```

Then hook it into your shell (add to `~/.zshrc` or `~/.bashrc`):

```
eval "$(direnv hook zsh)"   # or bash
```

Approve the `.envrc` once:

```
direnv allow
```

After that, `python`, `pytest`, etc. resolve to `.venv/bin/*` automatically whenever you're in this directory.
