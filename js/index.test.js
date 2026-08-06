import test from 'node:test';
import assert from 'node:assert';
import { readFile } from 'node:fs/promises';
import { refinedToCN, expandIterationMark } from './index.js';

// Minimal converters covering the characters exercised by tests/vectors.json.
const t2sMap = { '橋': '桥', '辺': '边', '邊': '边' };
const identity = (s) => s;
const converters = {
  jp2t: identity,
  t2s: (s) => [...s].map((c) => t2sMap[c] || c).join(''),
  tw2s: identity,
  hk2s: identity,
  t2jp: identity,
};

const vectors = JSON.parse(await readFile(new URL('../tests/vectors.json', import.meta.url), 'utf8'));

test('refinedToCN vectors', () => {
  for (const [raw, expected] of vectors) {
    assert.strictEqual(refinedToCN(raw, converters), expected, `${raw} -> ${expected}`);
  }
});

test('expandIterationMark', () => {
  assert.strictEqual(expandIterationMark('井々'), '井井');
});

test('refinedToCN idempotent across variants', () => {
  const cn = new Set(['澁谷', '渋谷', '涩谷'].map((x) => refinedToCN(x, converters)));
  assert.strictEqual(cn.size, 1);
});
