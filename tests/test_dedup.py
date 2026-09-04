from services.worker.app.pipeline.dedup import (
    canonicalize_url,
    content_hash,
    near_duplicate,
)


def test_canonicalize_url_removes_tracking_parameters() -> None:
    assert canonicalize_url("HTTPS://Example.com/story/?utm_source=x&id=2") == (
        "https://example.com/story?id=2"
    )


def test_content_hash_is_stable_after_whitespace_normalization() -> None:
    assert content_hash("a   headline") == content_hash("a headline")


def test_near_duplicate_text_is_detected() -> None:
    assert near_duplicate(
        "global market rises after policy news", "global market rises after policy news"
    )
