def importance_score(
    source_weight: float, report_count: int, impact: float, freshness: float
) -> float:
    """Stable baseline score; weights are intentionally explicit and tunable."""
    return round(
        0.35 * source_weight + 0.25 * min(report_count / 10, 1) + 0.25 * impact + 0.15 * freshness,
        6,
    )
