import msmtools.estimation
import msmtools.estimation.dense.ratematrix
import numpy as np
import scipy as sp
from msmtools.util import kahandot
import unittest
import msmtools
import warnings

class TestLowlevelNumerics(unittest.TestCase):
    def test_kdot(self):
       d0 = np.random.randint(1,high=100)
       d1 = np.random.randint(1,high=100)
       d2 = np.random.randint(1,high=100)
       a = np.random.randn(d0,d1)
       b = np.random.randn(d1,d2)
       assert np.allclose(a.dot(b), kahandot.kdot(a,b))

class TestEstimators(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        c = super(TestEstimators, cls).setUpClass()
        cls.tau = 0.001
        cls.K = np.array([[-1,    1,  0],
                          [100,-1100,1000],
                          [0,     5, -5]])
        cls.T = sp.linalg.expm(cls.tau*cls.K)
        cls.pi = msmtools.analysis.statdist(cls.T)
        cls.t_agg = 1000000 # 1M
        cls.C = np.ascontiguousarray(np.ceil(cls.pi[:,np.newaxis]*cls.T*cls.t_agg).astype(int))
        cls.C0 = np.zeros((3,3),dtype=int)
        cls.C0[0,1] = cls.C0[1,0] = cls.C0[1,2] = cls.C0[2,1] = 1

    def test_Kalbfleisch_Lawless_with_connectivity(self):
        est = msmtools.estimation.dense.ratematrix.KalbfleischLawlessEstimator(self.C, self.K, self.pi, dt=self.tau, sparsity=self.C0, t_agg=self.t_agg*self.tau, tol=100.0)
        K_est = est.run()
        assert np.allclose(self.K, K_est, rtol=5.0E-3)

    def test_Crommelin_Vanden_Eijnden_with_connectivity(self):
        est = msmtools.estimation.dense.ratematrix.CrommelinVandenEijndenEstimator(self.T, self.K, self.pi, dt=self.tau, sparsity=self.C0, t_agg=self.t_agg*self.tau, tol=100.0)
        K_est = est.run()
        assert np.allclose(self.K, K_est, rtol=5.0E-3)
        
    def test_api_with_connectivity_with_pi(self):
        K_est = msmtools.estimation.rate_matrix(self.C, dt=self.tau, sparsity=self.C0, t_agg=self.t_agg*self.tau, pi=self.pi, tol=100.0)
        assert np.allclose(self.K, K_est, rtol=5.0E-3)

    def test_api_without_connectivity_with_pi(self):
        K_est = msmtools.estimation.rate_matrix(self.C, dt=self.tau, pi=self.pi, tol=100.0)
        assert np.allclose(self.K, K_est, rtol=5.0E-3, atol=1.0E-3)

    def test_api_with_connectivity_without_pi(self):
        K_est = msmtools.estimation.rate_matrix(self.C, dt=self.tau, sparsity=self.C0, t_agg=self.t_agg*self.tau, tol=100.0)
        assert np.allclose(self.K, K_est, rtol=5.0E-3)

    def test_api_without_connectivity_without_pi(self):
        K_est = msmtools.estimation.rate_matrix(self.C, dt=self.tau, tol=100.0)
        assert np.allclose(self.K, K_est, rtol=5.0E-3, atol=1.0E-3)

    def test_api_with_connectivity_with_pi_with_guess(self):
        K_est = msmtools.estimation.rate_matrix(self.C, dt=self.tau, sparsity=self.C0, t_agg=self.t_agg*self.tau, pi=self.pi, tol=100.0, K0=self.K)
        assert np.allclose(self.K, K_est, rtol=5.0E-3)

    def test_api_without_connectivity_with_pi_with_guess(self):
        K_est = msmtools.estimation.rate_matrix(self.C, dt=self.tau, pi=self.pi, tol=100.0, K0=self.K)
        assert np.allclose(self.K, K_est, rtol=5.0E-3, atol=1.0E-3)

    def test_api_with_connectivity_without_pi_with_guess(self):
        K_est = msmtools.estimation.rate_matrix(self.C, dt=self.tau, sparsity=self.C0, t_agg=self.t_agg*self.tau, tol=100.0, K0=self.K)
        assert np.allclose(self.K, K_est, rtol=5.0E-3)

    def test_api_without_connectivity_without_pi_with_guess(self):
        K_est = msmtools.estimation.rate_matrix(self.C, dt=self.tau, tol=100.0, K0=self.K)
        assert np.allclose(self.K, K_est, rtol=5.0E-3, atol=1.0E-3)

    def test_raise(self):
        with self.assertRaises(msmtools.estimation.dense.ratematrix.NotConvergedError):
            msmtools.estimation.rate_matrix(self.C, dt=self.tau, method='CVE', maxiter=1, on_error='raise')

    def test_warn(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            msmtools.estimation.rate_matrix(self.C, dt=self.tau, method='CVE', maxiter=1, on_error='warn')
            assert len(w) == 1
            assert issubclass(w[-1].category, msmtools.estimation.dense.ratematrix.NotConvergedWarning)


if __name__ == '__main__':
    unittest.main()
