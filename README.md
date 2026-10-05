run bid-setup
    - should show in the "npx netlify dev" window "Local dev server ready: http://localhost:8888"

## Setting up a new convention
1. in convention.py, add the convention to the CONVENTION_TREE
2. Create a convention class is its own module (see ConventionBase)
```
class ConventionBase:
    @property
    def challenge(self) -> Challenge:
        """Build the question."""
        hand = self._get_hand()
        return Challenge(
            theme=CONVENTION_THEME,
            title=CONVENTION_TITLE,
            description=CONVENTION_DESCRIPTION,
            question=txt.WHAT_IS_YOUR_BID,
            hand_cards=hand.sorted_card_names,
            display_elements=["auction", "hand", "bidding_box"],
            correct_response=self._correct_reponse(hand).upper(),
        )

def challenge() -> Challenge:
    challenges = [
        ConventionBase(),
    ]
    return random.choice(challenges).challenge
```
3. In application.py import the class's challenge as xxx
4. Add xxx to the CONVENTION_FUNCTIONS dictionary using the convention's id as the key
