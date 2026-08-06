import json
from pathlib import Path

from opencc_cn_name import refined_to_cn

ROOT = Path(__file__).resolve().parent.parent
VECTORS = json.loads((ROOT / "tests" / "vectors.json").read_text(encoding="utf-8"))


def test_refined_to_cn_vectors():
    for raw, expected in VECTORS:
        assert refined_to_cn(raw) == expected, f"{raw} -> {expected}, got {refined_to_cn(raw)}"


def test_refined_to_cn_idempotent():
    # 澁谷 / 渋谷 / 涩谷 all normalize to the same simplified-CN form
    cn = {refined_to_cn(x) for x in ["澁谷", "渋谷", "涩谷"]}
    assert cn == {"涩谷"}