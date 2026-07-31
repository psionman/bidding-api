list:
    just --list

run arg1="":
    uv run src/manage.py runserver  {{arg1}}

test arg1="":
    uv run -m pytest {{arg1}}

bfgdealer_path := "/home/jeff/projects/bfg/bfgdealer"

dev-bfgdealer:
    uv add --editable {{bfgdealer_path}}
    uv sync
    uv run python -c "import bfgdealer; print(bfgdealer.__file__)"

prod-bfgdealer version="":
    uv remove bfgdealer
    uv add bfgdealer{{ if version != "" { ">=" + version } else { "" } }}
    uv sync
    uv run python -c "import bfgdealer; print(bfgdealer.__file__)"