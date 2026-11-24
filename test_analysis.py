import unittest, itertools, math
import numpy as np
from analysis import *
class TestACTF(unittest.TestCase):
    def setUp(self): self.p=list(profiles().values())
    def test_invalid_vectors(self):
        for x in ([0]*5,[0]*7,[0]*5+[float('nan')],[0]*5+[1.1],[0]*5+[-.1]):
            with self.assertRaises(ValueError): vector(x)
    def test_weights(self):
        for w in ([1]*6,[0]*6,[-1,2,0,0,0,0],[1,0]):
            with self.assertRaises(ValueError): distance(self.p[0],self.p[1],w)
    def test_normalization(self):
        np.testing.assert_allclose(normalize([0,20,40,60,80,100],100),np.arange(6)/5)
        with self.assertRaises(ValueError): normalize([0]*6,0)
    def test_all_pairs_scalar(self):
        for a,b in itertools.combinations(self.p,2):
            for w in WEIGHTS.values():
                expected=math.sqrt(math.fsum(wi*(float(x)-float(y))**2 for wi,x,y in zip(w,a,b)))
                self.assertAlmostEqual(distance(a,b,w),expected,places=13)
    def test_metric(self):
        for a,b,c in itertools.product(self.p,repeat=3):
            self.assertLessEqual(distance(a,c),distance(a,b)+distance(b,c)+1e-12)
            self.assertAlmostEqual(distance(a,b),distance(b,a))
            self.assertTrue(0<=distance(a,b)<=1)
        for a in self.p:self.assertEqual(distance(a,a),0)
    def test_bounds_collision(self):
        self.assertAlmostEqual(distance([0]*6,[1]*6),1)
        self.assertEqual(distance([0]*6,[1,0,0,0,0,0],[0,.2,.2,.2,.2,.2]),0)
    def test_reflection(self):
        np.testing.assert_allclose(reflect(np.array([-.2,.2,1.2,2.2])),[.2,.2,.8,.2])
    def test_reference_pair(self): self.assertAlmostEqual(distance(self.p[0],self.p[2]),math.sqrt(1.4762/6),places=13)
    def test_noise_determinism(self):
        n=noise(self.p[0],self.p[2]);self.assertEqual(n,noise(self.p[0],self.p[2]));self.assertEqual(len(n),10)
        for r in n:self.assertTrue(0<=r['mean']<=1)
if __name__=='__main__':unittest.main()
