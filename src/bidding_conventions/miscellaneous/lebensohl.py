import random

from bidding_conventions.constants import WHAT_IS_YOUR_BID
from bidding_conventions.descriptions import get_description
from bidding_conventions.question import Question

CONVENTION_TITLE = "Lebensohl"
CONVENTION_DESCRIPTION = get_description("lebensohl.html")


class OvercallOneNt:
    @property
    def question(self) -> Question:
        global last_response
        options = [item[1] for item in self.OPTIONS]
        return Question(
            theme=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            preamble=WHAT_IS_YOUR_BID,
            options=options,
            correct_response=correct_response,
            display_elements=["preamble", "auction"],
            auction=["1NT", "cursor"],
            dealer="E",
        )


def _random_holding() -> tuple[str, str]:
    # global last_response
    # while True:
    #     holding, correct_response = random.choice(OVERCALLERS_HOLDINGS)
    #     if correct_response == "P" or correct_response == last_response:
    #         continue
    #     random_minor = random.choice(["C", "D"])
    #     random_major = random.choice(["H", "S"])
    #     if RANDOM_MINOR in holding:
    #         holding[random_minor] = holding[RANDOM_MINOR]
    #         holding.pop(RANDOM_MINOR)
    #     if RANDOM_MAJOR in holding:
    #         holding[random_major] = holding[RANDOM_MAJOR]
    #         holding.pop(RANDOM_MAJOR)
    #     last_response = correct_response
    #     return holding, correct_response

    return {}, "1C"


def question() -> Question:
    classes = [
        OvercallOneNt(),
        # Overcaller(),
        # AdvancersBid(),
        # AdvancerInterpretation(),
    ]
    return random.choice(classes).question


last_response = None
