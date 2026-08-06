import { JP2T_EXCLUDE, T2S_EXCLUDE, VARIANT_MAP } from './data_gen.js';

/**
 * OpenCC-complement name conversion for Japanese person names → simplified
 * Chinese. Converter injection mirrors the wikiEpStaffRelate userscript
 * usage: callers pass the OpenCC.Converter instances they already load.
 */

/** Expand 々 to the previous character (e.g., 井々 → 井井). */
export function expandIterationMark(s) {
  let out = '';
  for (let i = 0; i < s.length; i++) {
    out += s[i] === '\u3005' ? (i > 0 ? s[i - 1] : '') : s[i];
  }
  return out;
}

function applyVariantMap(s) {
  return [...s].map((c) => VARIANT_MAP[c] || c).join('');
}

/**
 * Convert a Japanese person name to simplified Chinese.
 *
 * @param {string} name
 * @param {{jp2t: Function, t2s: Function, tw2s: Function, hk2s: Function, t2jp: Function}} converters
 *   The five OpenCC converters (each string→string).
 * @returns {string}
 */
export function refinedToCN(name, converters) {
  const { jp2t, t2s, tw2s, hk2s, t2jp } = converters;

  const expanded = expandIterationMark(name);
  const hasExcluded = [...expanded].some((c) => T2S_EXCLUDE.has(c));

  // jp2t per-char, skip known-bad chars, t2s the changed chars
  const chars = [];
  for (const c of expanded) {
    if (JP2T_EXCLUDE.has(c)) chars.push(c);
    else {
      const jp = jp2t(c);
      chars.push(jp !== c ? t2s(jp) : c);
    }
  }
  let result = chars.join('');

  // whole-string t2s for chars jp2t didn't touch
  if (result !== expanded && !hasExcluded) result = t2s(result);
  // t2s/tw2s/hk2s without any Japanese step
  if (result === expanded && !hasExcluded) result = t2s(expanded);
  if (result === expanded && !hasExcluded) result = tw2s(expanded);
  if (result === expanded && !hasExcluded) result = hk2s(expanded);
  // direct variant mapping for chars OpenCC doesn't handle
  if (result === expanded) result = applyVariantMap(result);
  // t2jp → t2s as last resort
  if (result === expanded) {
    const jpNew = t2jp(expanded);
    if (jpNew !== expanded && t2s(jpNew) !== jpNew) result = t2s(jpNew);
  }
  // apply variant map again in case OpenCC output still has variants
  result = applyVariantMap(result);
  return result;
}
