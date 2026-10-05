"""
Text module that merges psiutils.text.strings with project-level strings.

Usage:
    from text_module import Text

    txt = Text()
    print(txt.SELECT)   # Access as attribute
    print(txt.DELETE_PROMPT)
"""

from dataclasses import dataclass, field

from psiutils.text import Text as PsiText

YOU_ARE_NORTH = "You are N"
strings = {
    "SUB_TITLE_PREFIX": "Practice bidding with the",
    "SUB_TITLE_SUFFIX": "convention",
    "WHAT_IS_YOUR_BID": (f"{YOU_ARE_NORTH}; what is your bid?"),
    "WHAT_IS_PARTERS_HOLDING": (
        "With this auction, what is partner's (S) holding?"
    ),
    "WHAT_DOES_PARTNERS_BID_MEAN": (
        f"{YOU_ARE_NORTH}; what does partner's (S) bid mean?"
    ),
}


@dataclass
class Text:
    """Combines package-level (psiutils) and project-level strings.

    Attributes from `psiutils.text.strings` are loaded first, then overridden
    or extended by the local `strings` dictionary.
    """

    display: bool = field(default=False, repr=False)

    def __post_init__(self) -> None:
        """Populate the dataclass instance with string attributes."""
        # Load psiutils strings
        psi_text = PsiText()
        psi_strings = psi_text.strings
        for key, string in psi_strings.items():
            setattr(self, key, string)

        # Override or add project-level strings
        for key, string in strings.items():
            setattr(self, key, string)

        # Optionally display contents of `text`
        if self.display:
            psi_text.display(strings)
