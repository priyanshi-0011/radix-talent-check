
from backend.models import SKILL_CATEGORIES, validate_rating


def calculate_readiness(candidate_ratings, company_levels):
    """
    Calculate readiness and skill gaps for all 12 categories.

    Unknown candidate ratings produce an incomplete result.
    The final score uses unrounded values.
    """

    expected_codes = set(SKILL_CATEGORIES)

    if set(candidate_ratings) != expected_codes:
        raise ValueError("Candidate must provide exactly 12 skill ratings.")

    if set(company_levels) != expected_codes:
        raise ValueError("Company must provide exactly 12 skill requirements.")

    rows = []
    total_attainment = 0.0
    completeness = 0

    for code, skill_name in SKILL_CATEGORIES.items():
        candidate_level = candidate_ratings[code]
        required_level = company_levels[code]

        if not validate_rating(candidate_level):
            raise ValueError(f"Invalid candidate rating for {code}.")

        if (
            isinstance(required_level, bool)
            or not isinstance(required_level, (int, float))
            or not 1 <= required_level <= 10
        ):
            raise ValueError(f"Invalid company requirement for {code}.")

        if candidate_level is None:
            rows.append({
                "category_code": code,
                "skill_name": skill_name,
                "required_level": required_level,
                "candidate_level": None,
                "gap": None,
                "shortfall": None,
                "attainment": None,
                "contribution": None,
            })
            continue

        completeness += 1

        attainment = min(candidate_level / required_level, 1.0)
        shortfall = max(required_level - candidate_level, 0)
        gap = shortfall > 0
        contribution = 100 * attainment / 12

        total_attainment += attainment

        rows.append({
            "category_code": code,
            "skill_name": skill_name,
            "required_level": required_level,
            "candidate_level": candidate_level,
            "gap": gap,
            "shortfall": shortfall,
            "attainment": round(attainment, 4),
            "contribution": round(contribution, 4),
        })

    complete = completeness == 12

    return {
        "schema_version": "TEAM-V1",
        "source_mode": "synthetic",
        "status": "complete" if complete else "incomplete",
        "rating_completeness": completeness,
        "readiness_score": (
            round((total_attainment / 12) * 100, 1)
            if complete else None
        ),
        "skillset_gap": rows,
    }
