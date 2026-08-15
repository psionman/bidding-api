# src/bidding_conventions/__init__.py

"""Initialise the application."""

from importlib.metadata import metadata, version

from psiutils.utilities import psi_logger

# Distribution name (must match pyproject.toml `name =`)
__dist_name__ = "bidding-conventions-api"

# Import / short name (matches the directory under src/)
__app_name__ = "bidding_conventions"

logger = psi_logger(__app_name__)

meta = metadata(__dist_name__)
__summary__: str = meta["Summary"]
__version__: str = version(__dist_name__)

if "Author" in meta:
    __author__: str = meta["Author"]
else:
    __author__: str = "Not defined"
