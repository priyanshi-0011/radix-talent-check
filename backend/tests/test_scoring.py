
from backend.models import SKILL_CATEGORIES
from backend.benchmarks import SYNTHETIC_COMPANY
from backend.scoring import calculate_readiness


def test_all_ratings_four_gives_fifty_percent():
    ratings = {code: 4 for code in SKILL_CATEGORIES}
    levels = SYNTHETIC_COMPANY["levels"]

    result = calculate_readiness(ratings, levels)

    assert result["readiness_score"] == 50.0
    assert result["status"] == "complete"
    assert result["rating_completeness"] == 12
    assert len(result["skillset_gap"]) == 12


def test_all_ratings_eight_gives_one_hundred_percent():
    ratings = {code: 8 for code in SKILL_CATEGORIES}
    levels = SYNTHETIC_COMPANY["levels"]

    result = calculate_readiness(ratings, levels)

    assert result["readiness_score"] == 100.0
    assert all(row["gap"] is False for row in result["skillset_gap"])


def test_unknown_rating_makes_result_incomplete():
    ratings = {code: 4 for code in SKILL_CATEGORIES}
    ratings["COD"] = None
    levels = SYNTHETIC_COMPANY["levels"]

    result = calculate_readiness(ratings, levels)

    assert result["status"] == "incomplete"
    assert result["readiness_score"] is None
    assert result["rating_completeness"] == 11

    coding_row = next(
        row for row in result["skillset_gap"]
        if row["category_code"] == "COD"
    )
    assert coding_row["contribution"] is None
    assert coding_row["gap"] is None
