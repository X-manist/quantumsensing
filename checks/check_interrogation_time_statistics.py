import numpy as np
rng = np.random.default_rng(1)

# (a) Tracking-only telegraph model: sign of generator flips at Poisson rate G
def tau_samples(G, T, N=200000):
    out = np.empty(N)
    for i in range(N):
        t = 0.0; s = 1.0; acc = 0.0
        while True:
            dt = rng.exponential(1/G)
            if t + dt >= T:
                acc += s*(T-t); break
            acc += s*dt; t += dt; s = -s
        out[i] = acc
    return out
G=1.0
for T in [0.5, 2.0, 8.0]:
    tau = tau_samples(G, T, 60000)
    Etau = (1-np.exp(-2*G*T))/(2*G)
    Etau2 = T/G - (1-np.exp(-2*G*T))/(2*G**2)
    print(f"T={T}: MC E|tau|-free mean={tau.mean():.4f} (th {Etau:.4f});  E[tau^2]={np.mean(tau**2):.4f} (th {Etau2:.4f})")
# optimal agnostic rate
x = np.linspace(0.01, 10, 200000)
h = (1-np.exp(-x))**2/x
i = h.argmax()
print("agnostic: x*=2GT=%.4f, rate*Gamma=%.4f ; aware rate*Gamma -> 1 ; ratio=%.3f" % (x[i], h[i]/2, 1/(h[i]/2)))

# (b) latency model: flip at rate G, corrected after fixed delay d (flips during delay ignored)
def tau_latency(G, T, d, N=40000):
    out = np.empty(N)
    for i in range(N):
        t=0.0; acc=0.0
        while True:
            dt = rng.exponential(1/G)
            if t+dt >= T: acc += (T-t); break
            acc += dt; t += dt
            bad = min(d, T-t); acc -= bad; t += bad
            if t >= T: break
        out[i]=acc
    return out
G=1.0; d=0.05; T=200.0
tau = tau_latency(G,T,d)
m = (1-G*d)/(1+G*d)
print(f"latency: E[tau]/T={tau.mean()/T:.4f} (m={m:.4f}); E[tau^2]/T^2={np.mean(tau**2)/T**2:.4f} (m^2={m*m:.4f}); Var/T={tau.var()/T:.4f}")

# (c) Jensen: syndrome-aware vs agnostic FI at the optimal working point
p = rng.dirichlet(np.ones(6)); eta = rng.uniform(0.2,1,6); t = rng.uniform(0.3,1,6)
print("aware", np.sum(p*eta**2*t**2), ">= agnostic bound", np.sum(p*eta*t)**2)

# (d) Steane-code numbers of Ott et al.: rho = (d phi_mean/d eps)^2 / var
eps=1e-3
pp=1-7/4*eps**2; pm=7/4*eps**2; php=7/4*eps**3; phm=-3*eps
mean=pp*php+pm*phm; var=pp*php**2+pm*phm**2-mean**2
dmean=(-21/2)*eps**2
print("Steane mean/eps^3=%.4f var/eps^4=%.4f rho=%.4f"%(mean/eps**3,var/eps**4,dmean**2/var))
