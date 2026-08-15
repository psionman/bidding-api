from unittest.mock import patch

import pytest

from bidding_conventions.defence_of_one_nt.asptro import AdvancerInterpretation

advancer = AdvancerInterpretation()


class TestQuestion:
    def test_returns_question_object(self):
        q = advancer.question
        assert q is not None

    def test_correct_response_is_valid_option(self):
        valid_responses = [desc for _, desc in AdvancerInterpretation.OPTIONS]
        for _ in range(20):
            q = advancer.question
            assert q.correct_response in valid_responses

    def test_options_contains_all_descriptions(self):
        q = advancer.question
        expected = [desc for _, desc in AdvancerInterpretation.OPTIONS]
        assert q.options == expected

    def test_preamble_contains_partners_bid(self):
        for bid, _ in AdvancerInterpretation.OPTIONS:
            with patch("random.choice", return_value=(bid, "")):
                q = advancer.question
                assert bid in q.preamble

    @pytest.mark.parametrize("bid, expected", AdvancerInterpretation.OPTIONS)
    def test_correct_response_matches_bid(self, bid, expected):
        with patch("random.choice", return_value=(bid, expected)):
            q = advancer.question
            assert q.correct_response == expected

    @pytest.mark.parametrize(
        "bid, expected",
        [
            ("2C", "5/4 H and another"),
            ("2D", "5/4 S and another"),
            ("2H", "6H"),
            ("2S", "6S"),
            ("2NT", "5C and 5D"),
        ],
    )
    def test_all_bid_meanings(self, bid, expected):
        with patch("random.choice", return_value=(bid, expected)):
            q = advancer.question
            assert q.correct_response == expected
