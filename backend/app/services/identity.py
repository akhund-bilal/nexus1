import math
from difflib import SequenceMatcher


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def identity_confidence(seed: str, handle: str) -> float:
    sim = similarity(seed, handle)
    normalized = 1 / (1 + math.exp(-10 * (sim - 0.5)))
    return round(float(normalized), 3)
