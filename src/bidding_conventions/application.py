import random
from importlib.metadata import version

from bidding_conventions import __version__
from bidding_conventions.constants import PACKAGES
from bidding_conventions.convention import CONVENTION_TREE
from bidding_conventions.defence_of_one_nt.asptro import (
    challenge as asptro_challenge,
)
from bidding_conventions.defence_of_one_nt.multi_landy import (
    challenge as multi_landy_challenge,
)
from bidding_conventions.five_card_majors.opener import (
    challenge as fcm_opener_challenge,
)
from bidding_conventions.five_card_majors.responder import (
    challenge as fcm_responder_challenge,
)
from bidding_conventions.five_card_majors.two_way_checkback import (
    challenge as fcm_two_way_checkback_challenge,
)
from bidding_conventions.images import card_images
from bidding_conventions.miscellaneous.lebensohl import (
    challenge as lebensohl_challenge,
)

CONVENTION_FUNCTIONS = {
    # key must be the id in the CONVENTION_TREE
    "asptro": asptro_challenge,
    "multi-landy": multi_landy_challenge,
    # 'ghestem': _get_ghestem,
    # 'puppet-stayman': _get_puppet_stayman,
    "lebensohl": lebensohl_challenge,
    "five-cm-opener": fcm_opener_challenge,
    "five-cm-responder-bid-one": fcm_responder_challenge,
    "2-way-checkback": fcm_two_way_checkback_challenge,
}


# ─────────────────────────────
# Static / bootstrap
# ─────────────────────────────
def static_data(ip_address: str) -> dict[str, object]:
    """Return a dict of static data."""
    context = {
        "card_images": card_images,
        "versions": package_versions(),
    }
    return context


def get_conventions(params: dict) -> dict:
    """
    Return a hierarchical tree of bridge conventions.

    Parameters
    ----------
    params : dict
        Reserved for future use; currently unused.

    Returns
    -------
    dict
        A dictionary with a single key, 'conventions', whose value is a list
        of convention nodes.
    """
    return {"conventions": CONVENTION_TREE}


def conventions_selected(params: dict) -> dict:
    if not params["conventions"]:
        return {"error": "No convention selected"}

    for convention in params["conventions"]:
        if convention not in CONVENTION_FUNCTIONS:
            return {"error": "Invalid convention name"}

    challenge = CONVENTION_FUNCTIONS[random.choice(params["conventions"])]()
    return challenge.response


def package_versions():
    versions = {
        "api": __version__,
    }
    for package in PACKAGES:
        versions[package] = version(package)
    return versions
