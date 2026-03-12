from app.services.identity import identity_confidence


def test_identity_confidence_increases_with_similarity() -> None:
    high = identity_confidence("jane_doe", "jane_doe")
    low = identity_confidence("jane_doe", "x93lkzz")
    assert high > low
