list:
    just --list

run arg1="":
    uv run src/manage.py runserver {{arg1}}

test arg1="":
    uv run -m pytest {{arg1}}

test-api arg1="":
    uv run tests/api.py {{arg1}}

bfgdealer_path := "/home/jeff/projects/bfg/bfgdealer"
bridgeobjects_path := "/home/jeff/projects/bfg/bridgeobjects"

dev package:
    #!/usr/bin/env fish
    set path {{ if package == "bfgdealer" { bfgdealer_path } else if package == "bridgeobjects" { bridgeobjects_path } else { error("Unknown package: " + package) } }}
    uv add --editable $path
    uv sync
    uv run python -c "import {{package}}; print({{package}}.__file__)"

prod package version="":
    #!/usr/bin/env fish
    uv remove {{package}}
    uv add {{package}}{{ if version != "" { ">=" + version } else { "" } }}
    uv sync
    uv run python -c "import {{package}}; print({{package}}.__file__)"