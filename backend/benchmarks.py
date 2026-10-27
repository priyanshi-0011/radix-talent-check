
# Synthetic practice benchmark for RADIX Talent Check.
# These are fictional values, NOT official company requirements.

SYNTHETIC_COMPANY = {
    "schema_version": "TEAM-V1",
    "id": "synthetic-company-1",
    "company": "Synthetic Practice Co",
    "source_mode": "synthetic",
    "notice": "Invented teaching values. Not official company expectations.",
    "levels": {
        "COD": 8,
        "DSA": 8,
        "OOD": 8,
        "APTI": 8,
        "COMM": 8,
        "AI": 8,
        "CLOUD": 8,
        "SQL": 8,
        "SWE": 8,
        "SYSD": 8,
        "NETW": 8,
        "OS": 8,
    },
}


def get_synthetic_benchmark():
    """Return the fictional benchmark used for practice."""
    return SYNTHETIC_COMPANY.copy()


def get_real_benchmark_status():
    """Real company benchmarks are unavailable until an authorized source is configured."""
    return {
        "available": False,
        "source_mode": "real",
        "message": "Authorized organizer source is not configured",
    }
