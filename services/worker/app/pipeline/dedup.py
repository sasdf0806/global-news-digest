import hashlib
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from datasketch import MinHash

TRACKING_PARAMS = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "fbclid"}


def canonicalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    query = [(key, value) for key, value in parse_qsl(parts.query) if key not in TRACKING_PARAMS]
    return urlunsplit(
        (
            parts.scheme.lower(),
            parts.netloc.lower(),
            parts.path.rstrip("/"),
            urlencode(sorted(query)),
            "",
        )
    )


def content_hash(text: str) -> str:
    return hashlib.sha256(" ".join(text.split()).encode("utf-8")).hexdigest()


def _minhash(text: str, num_perm: int = 128) -> MinHash:
    signature = MinHash(num_perm=num_perm)
    for token in set(text.lower().split()):
        signature.update(token.encode("utf-8"))
    return signature


def near_duplicate(left: str, right: str, threshold: float = 0.8) -> bool:
    return _minhash(left).jaccard(_minhash(right)) >= threshold
