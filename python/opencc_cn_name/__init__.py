"""OpenCC-complement name conversion for Japanese person names → simplified Chinese.

This is a thin wrapper around OpenCC that applies the hand-maintained
corrections from this package's data tables (JP2T_EXCLUDE / T2S_EXCLUDE /
VARIANT_MAP) for characters OpenCC handles incorrectly in Japanese names.

The pipeline (matching wikiPersonCnName / wikiEpStaffRelate userscripts):

    jp2t per-char (skip JP2T_EXCLUDE) → t2s whole string
    → tw2s → hk2s (only if unchanged so far)
    → VARIANT_MAP → t2jp → t2s (last resort)
    → VARIANT_MAP (final)
"""

from __future__ import annotations

import opencc

from ._data import JP2T_EXCLUDE, T2S_EXCLUDE, VARIANT_MAP

_opencc_converters = None


def _get_converters():
    global _opencc_converters
    if _opencc_converters is None:
        _opencc_converters = (
            opencc.OpenCC("jp2t"),
            opencc.OpenCC("t2s"),
            opencc.OpenCC("tw2s"),
            opencc.OpenCC("hk2s"),
            opencc.OpenCC("t2jp"),
        )
    return _opencc_converters


def expand_iteration_mark(s: str) -> str:
    """Expand 々 to the previous character (e.g., 井々 → 井井)."""
    out = []
    for i, ch in enumerate(s):
        if ch == "\u3005":
            out.append(s[i - 1] if i > 0 else "")
        else:
            out.append(ch)
    return "".join(out)


def _apply_variant_map(s: str) -> str:
    return s.translate(VARIANT_MAP)


def refined_to_cn(name: str, converters=None) -> str:
    """Convert a Japanese person name to simplified Chinese.

    converters: optional 5-tuple of (jp2t, t2s, tw2s, hk2s, t2jp) OpenCC
    instances, for testability / reuse. Defaults to shared instances.
    """
    if converters is None:
        converters = _get_converters()
    cc_jp2t, cc_t2s, cc_tw2s, cc_hk2s, cc_t2jp = converters

    expanded = expand_iteration_mark(name)
    has_excluded = any(c in T2S_EXCLUDE for c in expanded)

    # jp2t per-char, skip known-bad chars, t2s the changed chars
    chars = []
    for c in expanded:
        if c in JP2T_EXCLUDE:
            chars.append(c)
        else:
            jp_c = cc_jp2t.convert(c)
            chars.append(cc_t2s.convert(jp_c) if jp_c != c else c)
    result = "".join(chars)

    # whole-string t2s for chars jp2t didn't touch
    if result != expanded and not has_excluded:
        result = cc_t2s.convert(result)
    # t2s/tw2s/hk2s without any Japanese step
    if result == expanded and not has_excluded:
        result = cc_t2s.convert(expanded)
    if result == expanded and not has_excluded:
        result = cc_tw2s.convert(expanded)
    if result == expanded and not has_excluded:
        result = cc_hk2s.convert(expanded)
    # direct variant mapping for chars OpenCC doesn't handle
    if result == expanded:
        result = _apply_variant_map(result)
    # t2jp → t2s as last resort
    if result == expanded:
        jp_new = cc_t2jp.convert(expanded)
        if jp_new != expanded and cc_t2s.convert(jp_new) != jp_new:
            result = cc_t2s.convert(jp_new)
    # apply variant map again in case OpenCC output still has variants
    result = _apply_variant_map(result)
    return result
