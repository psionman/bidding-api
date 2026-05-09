import random

from bidding_conventions.asptro import question as asptro_question
from bidding_conventions.five_card_majors.opener import (
    question as fcm_opener_question,
)
from bidding_conventions.five_card_majors.responder import (
    question as fcm_responder_question,
)

CONVENTION_FUNCTIONS = {
    "asptro": asptro_question,
    # 'multi-landy': _get_mutli_landy,
    # 'ghestem': _get_ghestem,
    # 'puppet-stayman': _get_puppet_stayman,
    # 'lebensohl': _get_lebensol,
    "five-cm-opener": fcm_opener_question,
    "five-cm-responder-bid-one": fcm_responder_question,
}


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
        of convention nodes. Each node has the following structure:

        - id (str): A URL-safe slug uniquely identifying the convention.
        - name (str): The human-readable name of the convention.
        - children (list): A list of child convention nodes in the same
          structure, or an empty list if the node is a leaf.
    """
    conventions = [
        {
            "id": "defence-of-1nt",
            "name": "Defence of 1NT",
            "children": [
                {"id": "asptro", "name": "Asptro", "children": []},
                {"id": "multi-landy", "name": "Multi-Landy", "children": []},
            ],
        },
        # {"id": "ghestem", "name": "Ghestem", "children": []},
        # {"id": "puppet-stayman", "name": "Puppet Stayman", "children": []},
        # {"id": "lebensohl", "name": "Lebensohl", "children": []},
        {
            "id": "five-card-majors",
            "name": "5 Card Majors",
            "children": [
                {
                    "id": "five-cm-opener",
                    "name": "Opening bids",
                    "children": [],
                },
                {
                    "id": "five-cm-responder-bid-one",
                    "name": "Responder's bid",
                    "children": [],
                },
            ],
            "any": True,
        },
    ]
    return {"conventions": conventions}


def conventions_selected(params: dict) -> dict:
    if not params["conventions"]:
        return {"error": "No convention selected"}

    for convention in params["conventions"]:
        if convention not in CONVENTION_FUNCTIONS:
            return {"error": "Invalid convention name"}

    question = CONVENTION_FUNCTIONS[random.choice(params["conventions"])]()
    return question.response
