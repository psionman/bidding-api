from unittest.mock import patch

import pytest

from bidding_conventions.defence_of_one_nt.asptro import (
    Overcaller,
)

overcaller = Overcaller()


class TestExtremePointsAdjustment:
    @pytest.mark.parametrize(
        "points, response, expected",
        [
            (9, "2C", "P"),  # below minimum
            (10, "2C", "2C"),  # minimum
            (15, "2C", "2C"),  # maximum
            (16, "2C", "X"),  # above maximum
            (5, "2H", "P"),  # well below minimum
            (20, "2H", "X"),  # well above maximum
        ],
    )
    def test_extreme_points_adjustment(self, points, response, expected):
        assert (
            Overcaller._extreme_points_adjustment(points, response) == expected
        )


# class TestRandomHolding:
#     def test_returns_tuple(self):
#         print("xxx")
#         holding, response = overcaller._random_holding()
#         print(f"{holding=}")
#         assert isinstance(holding, str)
#         assert isinstance(response, str)

# def test_response_is_valid_option(self):
#     for _ in range(20):
#         _, response = overcaller._random_holding()
#         assert response in Overcaller.OPTIONS


class TestRandomPoints:
    def test_points_in_range(self):
        for _ in range(50):
            points = overcaller._random_points()
            assert 9 <= points <= 15


class TestBuildPreamble:
    def test_preamble_contains_holding_and_points(self):
        preamble = overcaller._build_preamble("5H and 4S", 12)
        assert "5H and 4S" in preamble
        assert "12" in preamble


class TestQuestion:
    # def test_question_returns_question_object(self):
    #     q = overcaller.question
    #     assert q.correct_response in OVERCALLERS_HOLDINGS

    def test_low_points_always_pass(self):
        with patch.object(Overcaller, "_random_points", return_value=9):
            q = overcaller.question
            print(f"{q.correct_response=}")
            assert q.correct_response == "P"


#     def test_high_points_always_double(self):
#         with patch.object(Overcaller, "_random_points", return_value=16):
#             q = overcaller.question
#             assert q.correct_response == "X"

#     @pytest.mark.parametrize(
#         "holding, expected",
#         [
#             ("6H", "2H"),
#             ("6S", "2S"),
#             ("5C and 5D", "2NT"),
#             ("4H and 4S", "P"),
#         ],
#     )
#     def test_specific_holdings(self, holding, expected):
#         with patch.object(
#             Overcaller, "_random_holding", return_value=(holding, expected)
#         ):
#             with patch.object(Overcaller, "_random_points", return_value=12):
#                 q = overcaller.question
#                 assert q.correct_response == expected
