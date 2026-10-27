
from typing import Optional

# The 12 skill categories required by RADIX Module 4
SKILL_CATEGORIES = {
    "COD": "Coding",
    "DSA": "Data Structures & Algorithms",
    "OOD": "Object-Oriented Design",
    "APTI": "Aptitude",
    "COMM": "Communication",
    "AI": "Artificial Intelligence",
    "CLOUD": "Cloud",
    "SQL": "SQL",
    "SWE": "Software Engineering",
    "SYSD": "System Design",
    "NETW": "Networking",
    "OS": "Operating Systems",
}


def validate_rating(value: Optional[float]) -> bool:
    """Accept ratings from 1 to 10, or None for an unknown rating."""
    if value is None:
        return True

    # Do not accept True or False as numeric ratings.
    if isinstance(value, bool):
        return False

    if not isinstance(value, (int, float)):
        return False

    # Reject infinity and NaN.
    if value != value or value in (float("inf"), float("-inf")):
        return False

    return 1 <= value <= 10
