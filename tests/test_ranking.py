from services.worker.app.pipeline.ranking import importance_score


def test_importance_score_is_bounded_and_deterministic() -> None:
    assert importance_score(1, 10, 1, 1) == 1.0
    assert importance_score(0.5, 2, 0.4, 0.8) == 0.445
