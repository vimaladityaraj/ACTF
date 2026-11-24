import copy, json, math, unittest
from actf import *
class Exchange(unittest.TestCase):
    def setUp(self): self.a=synthetic('a',[.1,.2,.3,.4,.5,.6]); self.b=synthetic('b',[.9,.8,.7,.6,.5,.4])
    def test_roundtrip(self): self.assertEqual(loads(dumps(self.a)),self.a)
    def test_named_order(self):
        b=copy.deepcopy(self.a);b['coordinates']=dict(reversed(list(b['coordinates'].items())));self.assertEqual(distance(self.a,b),0)
    def test_bool(self):
        self.a['coordinates']['S']=True;self.assertRaises(ProfileError,validate,self.a)
    def test_string(self):
        self.a['coordinates']['S']='0.1';self.assertRaises(ProfileError,validate,self.a)
    def test_nan(self):
        self.a['coordinates']['S']=float('nan');self.assertRaises(ProfileError,validate,self.a)
    def test_blank(self):
        self.a['source']='  ';self.assertRaises(ProfileError,validate,self.a)
    def test_duplicate(self): self.assertRaises(ProfileError,loads,'{"a":1,"a":2}')
    def test_nonstandard(self): self.assertRaises(ProfileError,loads,'{"a":NaN}')
    def test_missing_key(self):
        del self.a['coordinates']['P'];self.assertRaises(ProfileError,validate,self.a)
    def test_outside(self):
        self.a['coordinates']['S']=1.1;self.assertRaises(ProfileError,validate,self.a)
    def test_bad_scale(self):
        self.a['protocol']['scale']['upper']=0;self.assertRaises(ProfileError,validate,self.a)
    def test_bad_window(self):
        self.a['protocol']['window_s']=[5,2];self.assertRaises(ProfileError,validate,self.a)
    def test_protocol(self):
        self.b['protocol']['language']='ta';self.assertRaises(ProfileError,distance,self.a,self.b)
    def test_kind(self):
        self.b['data_kind']='observed';self.assertRaises(ProfileError,distance,self.a,self.b)
    def test_null(self):
        self.a['coordinates']['S']=None;self.assertRaises(ProfileError,distance,self.a,self.b); l,u,k=bounds(self.a,self.b);self.assertEqual(k,5);self.assertGreater(u,l)
    def test_one_unknown_extrema(self):
        a=synthetic('a',[None,0,0,0,0,0]);b=synthetic('b',[.8,0,0,0,0,0]);l,u,k=bounds(a,b);self.assertEqual(l,0);self.assertAlmostEqual(u,.8/math.sqrt(6))
    def test_two_unknown(self):
        a=synthetic('a',[None]*6);b=synthetic('b',[None]*6);l,u,k=bounds(a,b);self.assertEqual(l,0);self.assertAlmostEqual(u,1);self.assertEqual(k,0)
    def test_normalize(self): self.assertAlmostEqual(normalize(5,0,10),.5);self.assertRaises(ProfileError,normalize,True,0,1)
    def test_weight(self): self.assertRaises(ProfileError,distance,self.a,self.b,[True,0,0,0,0,0])
    def test_observed_unknown_time(self):
        self.a['data_kind']=self.b['data_kind']='observed';self.assertRaises(ProfileError,distance,self.a,self.b)
