# Check: F_aware = lam^2 E_s[(E[r tau|s])^2] and F_what / F_aware = corr^2, on a hidden-Markov "tracking-only" model
# hidden sign chain sigma_t (flip prob p per step), noisy syndrome o_t = sigma_t flipped w.p. q, tau = sum_t sigma_t
import numpy as np
rng = np.random.default_rng(7)
Tn, p, q, N = 40, 0.03, 0.12, 300000
sig = np.ones((N, Tn)); flips = rng.random((N, Tn)) < p; flips[:,0] = False
sig = np.where(np.cumsum(flips, axis=1) % 2 == 0, 1.0, -1.0)
obs = sig * np.where(rng.random((N, Tn)) < q, -1.0, 1.0)
tau = sig.sum(1)
# forward-backward smoothing: P(sigma_t=+1 | o_{1:T})
def lik(o, s): return np.where(o == s, 1-q, q)
A = np.array([[1-p, p],[p, 1-p]])           # states: 0 -> +1, 1 -> -1
al = np.zeros((N, Tn, 2)); be = np.ones((N, Tn, 2))
e = np.stack([lik(obs, 1.0), lik(obs, -1.0)], axis=2)
a = np.array([1.0, 0.0]) * e[:,0,:]; a /= a.sum(1, keepdims=True); al[:,0] = a
for t in range(1, Tn):
    a = (al[:,t-1] @ A) * e[:,t]; a /= a.sum(1, keepdims=True); al[:,t] = a
for t in range(Tn-2, -1, -1):
    b = (be[:,t+1] * e[:,t+1]) @ A.T; b /= b.sum(1, keepdims=True); be[:,t] = b
post = al * be; post /= post.sum(2, keepdims=True)
w_opt  = (post[:,:,0] - post[:,:,1]).sum(1)              # posterior mean of tau  (soft, smoothed)
w_hard = np.where(post[:,:,0] > 0.5, 1.0, -1.0).sum(1)   # plug-in hard decision
w_raw  = obs.sum(1)                                      # raw syndrome sum
w_agn  = np.full(N, tau.mean())                          # syndrome-agnostic (constant weight)
F = lambda w: np.mean(w*tau)**2 / np.mean(w*w)
Fa = np.mean(w_opt**2)
print("check E[w_opt*tau]=E[w_opt^2]:", np.mean(w_opt*tau), Fa)
for name, w in [("posterior", w_opt), ("hard", w_hard), ("raw", w_raw), ("agnostic", w_agn)]:
    c2 = np.mean(w*w_opt)**2/(np.mean(w*w)*np.mean(w_opt**2))
    print(f"{name:10s} F/T^2={F(w)/Tn**2:.4f}  F/F_aware={F(w)/Fa:.4f}  corr^2={c2:.4f}")
print("ideal F/T^2 = 1 ; known-tau (noiseless syndrome) F/T^2 =", np.mean(tau**2)/Tn**2)
# direct simulation of estimator variance for the posterior weight
theta = 2e-3; B = 300; n = N // B
x = np.where(rng.random(N) < 0.5*(1+np.sin(theta*tau)), 1.0, -1.0)
for name, w in [("posterior", w_opt), ("hard", w_hard), ("agnostic", w_agn)]:
    est = np.array([np.sum(x[i*n:(i+1)*n]*w[i*n:(i+1)*n]) / (n*np.mean(w*tau)) for i in range(B)])
    print(f"{name:10s} mean est={est.mean():.5f} (true {theta})  n*Var={n*est.var():.5f}  1/F={1/F(w):.5f}")
