"""Regression tests for the release fixes and asymmetric completion bounds."""
import copy
import itertools
import json
import math
import random
import subprocess
import tempfile
import unittest
from pathlib import Path

from actf import AXES, ProfileError, bounds, distance, normalize, synthetic

ROOT = Path(__file__).resolve().parent


class ReleaseRegression(unittest.TestCase):
    def setUp(self):
        self.a = synthetic('a', [.1, .2, .3, .4, .5, .6])
        self.b = synthetic('b', [.9, .8, .7, .6, .5, .4])

    def js(self, a, b):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'records.json'
            p.write_text(json.dumps([a, b]), encoding='utf-8')
            return subprocess.run(['node', str(ROOT / 'compare.mjs'), str(p)],
                                  capture_output=True, text=True, check=False)

    def test_js_protocol_key_order(self):
        b = copy.deepcopy(self.b)
        b['protocol'] = dict(reversed(list(b['protocol'].items())))
        b['protocol']['scale'] = dict(reversed(list(b['protocol']['scale'].items())))
        b['coordinates'] = dict(reversed(list(b['coordinates'].items())))
        result = self.js(self.a, b)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertAlmostEqual(json.loads(result.stdout)[0]['Dn'], distance(self.a, b), places=14)

    def test_js_rejects_protocol_mismatch(self):
        self.b['protocol']['scale']['anchors'] = 'different'
        self.assertNotEqual(self.js(self.a, self.b).returncode, 0)

    def test_js_rejects_unknown_observed_timing(self):
        self.a['data_kind'] = self.b['data_kind'] = 'observed'
        self.assertNotEqual(self.js(self.a, self.b).returncode, 0)

    def test_js_rejects_null_coordinate(self):
        self.b['coordinates']['P'] = None
        self.assertNotEqual(self.js(self.a, self.b).returncode, 0)

    def test_extreme_normalization(self):
        lo, hi = -1.7e308, 1.7e308
        for value, expected in [(lo, 0), (0, .5), (hi, 1), (hi/2, .75)]:
            result = normalize(value, lo, hi)
            self.assertTrue(math.isfinite(result))
            self.assertAlmostEqual(result, expected, places=14)

    def test_normalization_invalid_numbers(self):
        for args in [(float('inf'), 0, 1), (float('nan'), 0, 1),
                     (0, 0, 0), (2, 0, 1), (10**400, 0, 10**401),
                     (10**20, 10**20, 10**20+1)]:
            with self.subTest(args=args):
                with self.assertRaises(ProfileError):
                    normalize(*args)

    def test_asymmetric_bounds_against_enumeration(self):
        rng = random.Random(20261124)
        for case in range(100):
            a = [None if rng.random() < .45 else rng.random() for _ in AXES]
            b = [None if rng.random() < .45 else rng.random() for _ in AXES]
            weights = [rng.random() for _ in AXES]
            weights = [w / sum(weights) for w in weights]
            # Candidate values include endpoints and the observed counterpart,
            # since a one-missing-coordinate minimum may be interior.
            choices = []
            for x, y, w in zip(a, b, weights):
                xs = [x] if x is not None else ([0, 1] if y is None else [0, 1, y])
                ys = [y] if y is not None else ([0, 1] if x is None else [0, 1, x])
                choices.append([w*(u-v)**2 for u,v in itertools.product(xs,ys)])
            values = [math.sqrt(sum(z)) for z in itertools.product(*choices)]
            lo, hi, known = bounds(synthetic('a', a), synthetic('b', b), weights)
            with self.subTest(case=case):
                self.assertAlmostEqual(lo, min(values), places=13)
                self.assertAlmostEqual(hi, max(values), places=13)
                self.assertEqual(known, sum(x is not None and y is not None for x,y in zip(a,b)))
