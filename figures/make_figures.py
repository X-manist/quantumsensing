"""Generate the figures of QEC_sensing_research_proposals.md.

Usage:  python3 figures/make_figures.py            (all figures)
        python3 figures/make_figures.py fig3 fig5  (selected figures)

Schematic figures (1a, 2, 3, 6, 7, 8a, 9) illustrate definitions.
Plotted curves (1b, 4, 8b) evaluate closed-form expressions quoted in the report.
Figure 5 is a Monte Carlo simulation of the hidden-Markov toy model (example E6).
"""
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, PathPatch, Polygon
from matplotlib.path import Path

OUT = os.path.dirname(os.path.abspath(__file__))

# ink, chrome and series colours
SURF, INK, INK2, MUTED = "#ffffff", "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, NEUTRAL = "#e1e0d9", "#c3c2b7", "#f3f2ef"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
BLUE_TINT, BLUE_EDGE = "#dbe9fb", "#86b6ef"
W = 6.85  # full text width in inches

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8, "mathtext.fontset": "dejavusans",
    "text.color": INK, "axes.labelcolor": INK2, "axes.edgecolor": AXIS, "axes.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False, "axes.titlesize": 8,
    "xtick.color": INK2, "ytick.color": INK2, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
    "xtick.major.size": 0, "ytick.major.size": 0, "xtick.minor.size": 0, "ytick.minor.size": 0,
    "grid.color": GRID, "grid.linewidth": 0.6, "lines.linewidth": 1.6, "lines.solid_capstyle": "round",
    "legend.frameon": False, "legend.fontsize": 7.5, "figure.facecolor": SURF, "savefig.facecolor": SURF,
    "svg.hashsalt": "qec-sensing",
})


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".svg"), metadata={"Date": None})
    plt.close(fig)
    print("wrote", name + ".svg")


def canvas(height, width=W):
    """A blank drawing area whose data units are inches."""
    fig = plt.figure(figsize=(width, height))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, title=None, body=None, fc=NEUTRAL, ec=AXIS, tsize=8, bsize=7.2, lw=0.8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.07",
                                fc=fc, ec=ec, lw=lw, zorder=2))
    if title and body:
        ax.text(x + w / 2, y + h - 0.13, title, ha="center", va="top", fontsize=tsize,
                fontweight="bold", zorder=3)
        ax.text(x + w / 2, y + (h - 0.30) / 2 + 0.02, body, ha="center", va="center", fontsize=bsize,
                color=INK2, zorder=3, linespacing=1.35)
    elif title:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center", fontsize=tsize,
                fontweight="bold", zorder=3, linespacing=1.3)
    elif body:
        ax.text(x + w / 2, y + h / 2, body, ha="center", va="center", fontsize=bsize,
                color=INK2, zorder=3, linespacing=1.35)


def arrow(ax, pts, color=INK2, lw=1.0, head=8):
    """Polyline through pts ending in an arrow head."""
    pts = [tuple(p) for p in pts]
    if len(pts) > 2:
        xs, ys = zip(*pts[:-1])
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="butt", solid_joinstyle="round", zorder=4)
    ax.annotate("", xy=pts[-1], xytext=pts[-2], zorder=4,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=head,
                                shrinkA=0, shrinkB=0))


def style_axes(ax, grid="both"):
    ax.set_axisbelow(True)
    ax.grid(True, which="major", axis=grid)
    ax.minorticks_off()


# ----------------------------------------------------------------------------------------------
def fig1():
    """HNLS geometry and the scaling of the Fisher information."""
    fig = plt.figure(figsize=(W, 2.85))
    a = fig.add_axes([0.0, 0.0, 0.44, 1.0])
    a.set_xlim(0, 3.0)
    a.set_ylim(0, 2.85)
    a.axis("off")
    a.text(0.08, 2.68, "(a)", fontweight="bold", va="center")
    o, tip = np.array([0.45, 0.72]), np.array([2.25, 2.2])
    a.plot([0.15, 2.9], [o[1], o[1]], color=AXIS, lw=1.2, zorder=1)
    a.text(2.9, o[1] - 0.14, r"Lindblad span $\mathcal{S}$", ha="right", va="top", fontsize=8)
    a.text(2.9, o[1] - 0.34, "(everything the noise can generate)", ha="right", va="top",
           fontsize=6.8, color=INK2)
    arrow(a, [o, (tip[0], o[1])], color=MUTED, lw=1.6, head=9)
    arrow(a, [(tip[0], o[1]), tip], color=BLUE, lw=2.2, head=11)
    arrow(a, [o, tip], color=INK, lw=1.3, head=10)
    a.plot([tip[0] - 0.13, tip[0] - 0.13, tip[0]], [o[1], o[1] + 0.13, o[1] + 0.13], color=MUTED, lw=0.7)
    a.text(1.08, 1.56, r"$G$", fontsize=10, ha="right")
    a.text(0.93, 1.38, "signal\ngenerator", fontsize=6.8, color=INK2, ha="right", va="top", linespacing=1.25)
    a.text(0.86, o[1] + 0.09, r"$G_\parallel$", fontsize=9, ha="center", va="bottom")
    a.text(1.0, o[1] + 0.12, "removed with the noise", fontsize=6.6, color=INK2, ha="left", va="bottom")
    a.text(tip[0] + 0.1, 1.55, r"$G_\perp$", fontsize=10, va="center")
    a.text(tip[0] + 0.1, 1.31, "survives\nerror\ncorrection", fontsize=6.8, color=INK2, va="top", linespacing=1.25)
    a.text(0.45, 2.42, r"HNLS condition:  $G_\perp\neq 0$", fontsize=8, va="center")

    b = fig.add_axes([0.535, 0.155, 0.445, 0.735])
    T = np.logspace(-2, 5, 500)

    def total_fi(T, rate):  # best repetition of Ramsey cycles with contrast exp(-rate * t)
        return np.where(T <= 0.5 / rate, T**2 * np.exp(-2 * rate * T), T / (2 * np.e * rate))

    b.loglog(T, T**2, color=AXIS, lw=1.2, label="noiseless reference")
    b.loglog(T, total_fi(T, 1.0), color=ORANGE, label=r"unencoded sensor, noise rate $\Gamma$")
    b.loglog(T, total_fi(T, 1e-3), color=BLUE, label=r"error-corrected, residual rate $10^{-3}\Gamma$")
    style_axes(b)
    b.set_xlim(1e-2, 1e5)
    b.set_ylim(1e-4, 1e10)
    b.set_xticks([1e-2, 1, 1e2, 1e4])
    b.set_yticks([1e-4, 1, 1e4, 1e8])
    b.set_xlabel(r"total sensing time $\Gamma T$")
    b.set_ylabel(r"Fisher information $\Gamma^2F$")
    b.legend(loc="upper left", handlelength=1.6, borderaxespad=0.2, labelspacing=0.35)
    b.text(3e3, 3.0e8, r"$\propto T^2$", fontsize=8, color=INK2, ha="right")
    b.text(2.5e4, 2.0e2, r"$\propto T$", fontsize=8, color=INK2, ha="center")
    b.plot([500, 500], [1e-4, 500**2 * np.exp(-1)], color=MUTED, lw=0.7)
    b.text(650, 3e-3, r"$T^\star$", fontsize=8.5, color=INK, va="center")
    fig.text(0.475, 0.94, "(b)", fontweight="bold", va="center")
    save(fig, "fig1_hnls")


# ----------------------------------------------------------------------------------------------
def fig2():
    """Pipeline of an error-corrected sensing protocol and the open layer."""
    fig, ax = canvas(3.35)
    yq, hq = 2.0, 0.78   # quantum row
    yc, hc = 0.62, 0.78  # classical row
    ax.text(0.12, 3.17, "QUANTUM LAYER", fontsize=7, fontweight="bold", color=INK2, va="center")
    ax.text(1.36, 3.17, "fixed by the code: established theory (HNLS, optimal codes, thresholds)",
            fontsize=7, color=INK2, va="center")
    box(ax, 0.12, yq, 1.2, hq, "Encoded probe", r"logical state $|\bar{+}\rangle$")
    box(ax, 1.75, yq, 1.4, hq, "Interrogation", r"signal $e^{-i\theta G\,\delta t}$" + "\nplus noise")
    box(ax, 3.58, yq, 1.3, hq, "Syndrome\nmeasurement")
    box(ax, 5.5, yq, 1.22, hq, "Logical readout", r"outcome $x=\pm1$")
    arrow(ax, [(1.32, yq + hq / 2), (1.75, yq + hq / 2)])
    arrow(ax, [(3.15, yq + hq / 2), (3.58, yq + hq / 2)])
    arrow(ax, [(4.88, yq + hq / 2), (5.5, yq + hq / 2)])
    arrow(ax, [(4.23, yq + hq), (4.23, yq + hq + 0.2), (2.45, yq + hq + 0.2), (2.45, yq + hq)], color=MUTED)
    ax.text(4.33, yq + hq + 0.1, r"repeat every $\delta t$", fontsize=6.8, color=INK2, ha="left", va="center")

    box(ax, 1.75, yc, 1.4, hc, "Recovery", "action on the sensor", fc=BLUE_TINT, ec=BLUE_EDGE)
    box(ax, 3.58, yc, 1.3, hc, "Decoder", r"inference from $s$", fc=BLUE_TINT, ec=BLUE_EDGE)
    box(ax, 5.5, yc, 1.22, hc, "Estimator", r"$\hat\theta(s,x)$", fc=BLUE_TINT, ec=BLUE_EDGE)
    arrow(ax, [(4.23, yq), (4.23, yc + hc)])
    ax.text(4.31, (yq + yc + hc) / 2, r"syndrome record $s$", fontsize=6.8, color=INK2, va="center")
    arrow(ax, [(3.58, yc + hc / 2), (3.15, yc + hc / 2)])
    arrow(ax, [(2.45, yc + hc), (2.45, yq)])
    ax.text(2.37, (yq + yc + hc) / 2, "real-time\nfeedback", fontsize=6.8, color=INK2, va="center", ha="right",
            linespacing=1.25)
    arrow(ax, [(4.88, yc + hc / 2), (5.5, yc + hc / 2)], color=BLUE, lw=2.0, head=11)
    arrow(ax, [(6.11, yq), (6.11, yc + hc)])
    ax.text(6.19, (yq + yc + hc) / 2, r"$x$", fontsize=8, color=INK2, va="center")
    ax.text(5.19, yc + hc / 2 - 0.13, "whole\nrecord", fontsize=6.4, color=INK2, ha="center", va="top",
            linespacing=1.2)

    ax.text(0.12, 0.33, "CLASSICAL LAYER", fontsize=7, fontweight="bold", color=INK2, va="center")
    ax.text(1.42, 0.33, "open: what must be inferred (P1), when to act (P2), how to score it (P3), "
            "how to learn it (P7)", fontsize=7, color=INK2, va="center")
    ax.add_patch(FancyBboxPatch((0.12, 0.06), 0.16, 0.11, boxstyle="round,pad=0,rounding_size=0.02",
                                fc=BLUE_TINT, ec=BLUE_EDGE, lw=0.8))
    ax.text(0.36, 0.115, "components without a sensing-specific theory", fontsize=6.8, color=INK2, va="center")
    ax.plot([3.3, 3.6], [0.115, 0.115], color=BLUE, lw=2.0)
    ax.text(3.68, 0.115, "syndrome-aware path: the record also reaches the estimator",
            fontsize=6.8, color=INK2, va="center")
    save(fig, "fig2_pipeline")


# ----------------------------------------------------------------------------------------------
def fig3():
    """Gain and signed interrogation time for three error histories."""
    T = 10.0
    cases = [
        (r"(a) class T, recovery after delay $\tau_d$", [(0, 4, 1), (4, 5.5, -1), (5.5, T, 1)],
         [(4, "error", "right"), (5.5, "recovery", "left")]),
        ("(b) class T, no recovery (tracked)", [(0, 3, 1), (3, 4.5, -1), (4.5, 8, 1), (8, T, -1)],
         [(3, "errors", "right"), (4.5, None, None), (8, None, None)]),
        ("(c) class P", [(0, T, 1)], [(6, "error", "right")]),
    ]
    fig, axes = plt.subplots(2, 3, figsize=(W, 3.55), sharex=True,
                             gridspec_kw=dict(height_ratios=[1, 1.3], hspace=0.16, wspace=0.14,
                                              left=0.085, right=0.985, top=0.9, bottom=0.2))
    for j, (title, segs, events) in enumerate(cases):
        g, s = axes[0, j], axes[1, j]
        for t0, t1, v in segs:
            g.fill_between([t0, t1], 0, v, color=BLUE if v > 0 else ORANGE, alpha=0.16 if v > 0 else 0.22, lw=0)
        ts = [segs[0][0]] + [t for seg in segs for t in (seg[1],)]
        vs = [seg[2] for seg in segs]
        g.step(ts, vs + [vs[-1]], where="post", color=BLUE, lw=1.6)
        g.axhline(0, color=AXIS, lw=0.8)
        g.set_ylim(-1.45, 2.05)
        g.set_yticks([-1, 0, 1])
        g.set_title(title, loc="left", pad=5, fontsize=7.6, fontweight="bold")
        g.spines["bottom"].set_visible(False)
        for t, lab, ha in events:
            g.plot([t], [1.42], marker="v", ms=5, color=INK, clip_on=False)
            if lab:
                g.text(t + (-0.3 if ha == "right" else 0.3), 1.42, lab, fontsize=6.8, color=INK2, ha=ha, va="center")
        # running integral
        tt = np.linspace(0, T, 801)
        gain = np.zeros_like(tt)
        for t0, t1, v in segs:
            gain[(tt >= t0) & (tt <= t1)] = v
        acc = np.concatenate([[0], np.cumsum((gain[1:] + gain[:-1]) / 2 * np.diff(tt))])
        s.plot(tt, tt, color=AXIS, lw=1.2)
        s.plot(tt, acc, color=BLUE)
        s.plot([T], [acc[-1]], marker="o", ms=5.5, color=BLUE, mec=SURF, mew=1.2, clip_on=False, zorder=5)
        s.set_ylim(-0.6, 11.4)
        s.set_yticks([0, 5, 10])
        s.set_xlim(0, T)
        s.set_xticks([0, 5, 10])
        s.set_xticklabels(["0", "", r"$T$"])
        style_axes(s, "y")
        style_axes(g, "y")
        s.set_xlabel(r"time $t$")
        tau = acc[-1]
        if j == 2:
            s.text(9.7, 3.3, r"$\tau=T$", fontsize=8, ha="right", va="center")
            s.text(9.7, 2.3, "outcome sign flipped\n" + r"($r=-1$), fixed in software", fontsize=6.8, color=INK2,
                   ha="right", va="top", linespacing=1.3)
        elif j == 0:
            s.text(9.7, 2.1, r"$\tau=T-2\tau_d$", fontsize=8, ha="right", va="center")
        else:
            s.text(9.7, 0.9, r"$\tau=0.3\,T$", fontsize=8, ha="right", va="center")
        if j > 0:
            g.tick_params(labelleft=False)
            s.tick_params(labelleft=False)
    axes[0, 0].set_ylabel(r"gain $g(E(t))$")
    axes[1, 0].set_ylabel(r"$\int_0^t g\,\mathrm{d}t'$")
    # legend
    lx = 0.085
    fig.patches.append(plt.Rectangle((lx, 0.035), 0.022, 0.03, transform=fig.transFigure, fc=BLUE, alpha=0.3, lw=0))
    fig.text(lx + 0.03, 0.05, r"adds to $\tau$", fontsize=7, color=INK2, va="center")
    fig.patches.append(plt.Rectangle((lx + 0.15, 0.035), 0.022, 0.03, transform=fig.transFigure, fc=ORANGE,
                                     alpha=0.4, lw=0))
    fig.text(lx + 0.18, 0.05, r"subtracts from $\tau$", fontsize=7, color=INK2, va="center")
    fig.lines.append(plt.Line2D([lx + 0.36, lx + 0.39], [0.05, 0.05], transform=fig.transFigure, color=BLUE, lw=1.6))
    fig.text(lx + 0.398, 0.05, "with errors", fontsize=7, color=INK2, va="center")
    fig.lines.append(plt.Line2D([lx + 0.51, lx + 0.54], [0.05, 0.05], transform=fig.transFigure, color=AXIS, lw=1.2))
    fig.text(lx + 0.548, 0.05, "error-free reference", fontsize=7, color=INK2, va="center")
    save(fig, "fig3_interrogation_time")


# ----------------------------------------------------------------------------------------------
def fig4():
    """Fisher information versus interrogation time for four recovery / inference policies."""
    fig = plt.figure(figsize=(W, 3.0))
    ax = fig.add_axes([0.085, 0.15, 0.52, 0.8])
    T = np.logspace(-1.3, 2.5, 500)
    gbar = (1 - 0.1) / (1 + 0.1)
    curves = [
        ("ideal", T**2, AXIS, 1.2),
        ("latency", gbar**2 * T**2, BLUE, 1.6),
        ("aware", T - (1 - np.exp(-2 * T)) / 2, ORANGE, 1.6),
        ("agnostic", ((1 - np.exp(-2 * T)) / 2) ** 2, AQUA, 1.6),
    ]
    for _, y, c, lw in curves:
        ax.loglog(T, y, color=c, lw=lw)
    style_axes(ax)
    ax.set_xlim(T[0], T[-1])
    ax.set_ylim(1e-3, 3e5)
    ax.set_xticks([0.1, 1, 10, 100])
    ax.set_xticklabels(["0.1", "1", "10", "100"])
    ax.set_yticks([1e-2, 1, 1e2, 1e4])
    ax.set_xlabel(r"interrogation time $\Gamma T$")
    ax.set_ylabel(r"Fisher information $\Gamma^2F/\lambda^2$")
    labels = [
        (T[-1] ** 2, 2.2e5, AXIS, "ideal instantaneous recovery", r"$F=\lambda^2T^2$"),
        (gbar**2 * T[-1] ** 2, 1.1e4, BLUE, r"recovery delayed by $\tau_d=0.1/\Gamma$",
         r"$F\simeq\bar g^2\lambda^2T^2$,  $\bar g=0.82$"),
        (T[-1], 3.0e2, ORANGE, "no recovery, errors tracked", r"$F\to\lambda^2T/\Gamma$"),
        (0.25, 0.25, AQUA, "no recovery, syndromes ignored", r"$F\to\lambda^2/4\Gamma^2$"),
    ]
    xe = T[-1]
    for yend, ylab, c, l1, l2 in labels:
        ax.plot([xe * 1.08, xe * 1.9, xe * 2.6], [yend, ylab, ylab], color=c, lw=1.2, clip_on=False,
                solid_capstyle="butt")
        ax.plot([xe], [yend], marker="o", ms=5, color=c, mec=SURF, mew=1.0, clip_on=False, zorder=6)
        ax.text(xe * 3.0, ylab, l1, fontsize=7.4, va="bottom", ha="left", color=INK)
        ax.text(xe * 3.0, ylab, l2, fontsize=7.4, va="top", ha="left", color=INK2)
    save(fig, "fig4_fisher_vs_time")


# ----------------------------------------------------------------------------------------------
def hmm_weights(n_shots=120000, steps=40, p=0.03, q=0.12, seed=7):
    """Tracking-only toy model: hidden sign chain, noisy syndromes, exact posterior by smoothing."""
    rng = np.random.default_rng(seed)
    flips = rng.random((n_shots, steps)) < p
    flips[:, 0] = False
    sig = np.where(np.cumsum(flips, axis=1) % 2 == 0, 1.0, -1.0)
    obs = sig * np.where(rng.random((n_shots, steps)) < q, -1.0, 1.0)
    tau = sig.sum(1)
    A = np.array([[1 - p, p], [p, 1 - p]])
    e = np.stack([np.where(obs == 1.0, 1 - q, q), np.where(obs == -1.0, 1 - q, q)], axis=2)
    al = np.zeros((n_shots, steps, 2))
    be = np.ones((n_shots, steps, 2))
    a = np.array([1.0, 0.0]) * e[:, 0, :]
    al[:, 0] = a / a.sum(1, keepdims=True)
    for t in range(1, steps):
        a = (al[:, t - 1] @ A) * e[:, t]
        al[:, t] = a / a.sum(1, keepdims=True)
    for t in range(steps - 2, -1, -1):
        b = (be[:, t + 1] * e[:, t + 1]) @ A.T
        be[:, t] = b / b.sum(1, keepdims=True)
    post = al * be
    post /= post.sum(2, keepdims=True)
    w = (post[:, :, 0] - post[:, :, 1]).sum(1)
    w_hard = np.where(post[:, :, 0] > 0.5, 1.0, -1.0).sum(1)
    return steps, tau, w, w_hard, obs.sum(1)


def fig5():
    """Distribution of posterior weights and Fisher information retained by cheaper decoders."""
    steps, tau, w, w_hard, w_raw = hmm_weights()
    f_aware = np.mean(w**2)
    retained = lambda v: np.mean(v * tau) ** 2 / np.mean(v * v) / f_aware
    vals = [1.0, retained(w_hard), retained(w_raw), tau.mean() ** 2 / f_aware]
    names = [r"posterior mean $w(s)$", "hard decision per step", "raw syndrome sum", "constant (syndromes ignored)"]

    fig = plt.figure(figsize=(W, 2.75))
    a = fig.add_axes([0.075, 0.17, 0.4, 0.71])
    edges = np.linspace(-1, 1, 41)
    h, _ = np.histogram(w / steps, bins=edges)
    a.bar(edges[:-1], h / len(w), width=np.diff(edges), align="edge", color=BLUE, ec=SURF, lw=0.7)
    m = tau.mean() / steps
    a.plot([m, m], [0, 0.2], color=INK2, lw=1.0)
    a.text(m - 0.05, 0.2, "single weight used when\nsyndromes are ignored", fontsize=6.8, color=INK2,
           va="top", ha="right", linespacing=1.3)
    top = h[-1] / len(w)
    a.text(0.93, top, "shots with no\nerror inferred", fontsize=6.8, color=INK2, va="top", ha="right",
           linespacing=1.3)
    style_axes(a, "y")
    a.set_xlim(-1, 1)
    a.set_ylim(0, 0.34)
    a.set_yticks([0, 0.1, 0.2, 0.3])
    a.set_xticks([-1, -0.5, 0, 0.5, 1])
    a.set_xlabel(r"posterior weight of a shot, $w(s)/T$")
    a.set_ylabel("fraction of shots")
    a.set_title("(a) each shot carries a different weight", loc="left", fontweight="bold", fontsize=7.6, pad=6)

    b = fig.add_axes([0.575, 0.17, 0.4, 0.71])
    hbar = 0.34
    for i, v in enumerate(vals):
        y = len(vals) - 1 - i
        r = 0.022
        verts = [(0, y - hbar / 2), (v - r, y - hbar / 2), (v, y - hbar / 2), (v, y - hbar / 2 + 0.11),
                 (v, y + hbar / 2 - 0.11), (v, y + hbar / 2), (v - r, y + hbar / 2), (0, y + hbar / 2), (0, y - hbar / 2)]
        codes = [Path.MOVETO, Path.LINETO, Path.CURVE3, Path.CURVE3, Path.LINETO, Path.CURVE3, Path.CURVE3,
                 Path.LINETO, Path.CLOSEPOLY]
        b.add_patch(PathPatch(Path(verts, codes), fc=BLUE, lw=0, zorder=3))
        b.text(0, y + hbar / 2 + 0.07, names[i], fontsize=7.4, va="bottom", ha="left", color=INK)
        txt = f"{100 * v:.1f}%" if 0.9 < v < 0.9995 else f"{100 * v:.0f}%"
        if v > 0.8:
            b.text(v - 0.025, y, txt, fontsize=7.4, va="center", ha="right", color="#ffffff", zorder=4)
        else:
            b.text(v + 0.025, y, txt, fontsize=7.4, va="center", ha="left", color=INK, zorder=4)
    b.set_xlim(0, 1.0)
    b.set_ylim(-0.45, len(vals) - 0.25)
    b.set_yticks([])
    b.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    b.set_xticklabels(["0", "25%", "50%", "75%", "100%"])
    b.spines["left"].set_color(AXIS)
    style_axes(b, "x")
    b.set_xlabel(r"Fisher information retained, $\mathrm{corr}^2(\hat w,w)$")
    b.set_title("(b) what a cheaper decoder output costs", loc="left", fontweight="bold", fontsize=7.6, pad=6)
    save(fig, "fig5_decoder_weights")
    print("   retained:", [round(float(v), 4) for v in vals], " F_aware/T^2 =", round(float(f_aware) / steps**2, 4))


# ----------------------------------------------------------------------------------------------
def fig6():
    """Logical fidelity versus metrological fidelity, and the three-factor decomposition."""
    fig, ax = canvas(3.55)
    x0, y0, cw, ch, gap = 0.95, 1.5, 2.85, 0.82, 0.1
    cells = [
        (0, 1, True, "Known frame or known gain",
         "the state differs from the ideal one,\nbut by a known map: nothing is lost"),
        (1, 1, False, "Ideal error-corrected sensor", "noise removed, signal kept"),
        (0, 0, False, "Uncorrected noise", "state and signal both degraded"),
        (1, 0, True, "Over-protective code",
         "the code also removes the signal:\n" + r"$\Pi G\Pi\propto\Pi$, fidelity 1, information 0"),
    ]
    for cx, cy, hi, title, body in cells:
        bx, by = x0 + cx * (cw + gap), y0 + cy * (ch + gap)
        box(ax, bx, by, cw, ch, fc=BLUE_TINT if hi else NEUTRAL, ec=BLUE_EDGE if hi else AXIS)
        ax.text(bx + 0.14, by + ch - 0.17, title, fontsize=8, fontweight="bold", va="top")
        ax.text(bx + 0.14, by + ch - 0.42, body, fontsize=7.2, color=INK2, va="top", linespacing=1.35)
    arrow(ax, [(x0, y0 - 0.14), (x0 + 2 * cw + gap, y0 - 0.14)], color=MUTED)
    ax.text(x0 + cw + gap / 2, y0 - 0.2, "logical fidelity to the ideal channel", fontsize=7.4, color=INK2,
            ha="center", va="top")
    ax.text(x0, y0 - 0.2, "low", fontsize=7, color=MUTED, ha="left", va="top")
    ax.text(x0 + 2 * cw + gap, y0 - 0.2, "high", fontsize=7, color=MUTED, ha="right", va="top")
    arrow(ax, [(x0 - 0.14, y0), (x0 - 0.14, y0 + 2 * ch + gap)], color=MUTED)
    ax.text(x0 - 0.3, y0 + ch + gap / 2, r"information about $\theta$", fontsize=7.4, color=INK2, rotation=90,
            ha="center", va="center")
    ax.text(x0 - 0.2, y0, "low", fontsize=7, color=MUTED, ha="right", va="bottom")
    ax.text(x0 - 0.2, y0 + 2 * ch + gap, "high", fontsize=7, color=MUTED, ha="right", va="top")
    ax.add_patch(FancyBboxPatch((x0, y0 + 2 * ch + gap + 0.13), 0.16, 0.11,
                                boxstyle="round,pad=0,rounding_size=0.02", fc=BLUE_TINT, ec=BLUE_EDGE, lw=0.8))
    ax.text(x0 + 0.24, y0 + 2 * ch + gap + 0.185, "the two measures disagree", fontsize=7, color=INK2, va="center")

    yb, hb = 0.12, 0.72
    ax.text(0.5, yb + hb / 2, r"$\mathcal{F}_{\mathrm{met}}\;=$", fontsize=10, ha="center", va="center")
    parts = [("code", r"$(\lambda/\lambda_0)^2$" + "\nsignal retention"),
             ("noise and action", r"$\mathbb{E}[w^2]/T^2$" + "\ngain kept by the recovery"),
             ("inference", r"$\mathrm{corr}^2(\hat w,w)$" + "\ndecoder quality")]
    bw, sep = 1.72, 0.25
    for i, (t, bdy) in enumerate(parts):
        bx = x0 + i * (bw + sep)
        box(ax, bx, yb, bw, hb, t, bdy, bsize=7.2)
        if i < 2:
            ax.text(bx + bw + sep / 2, yb + hb / 2, r"$\times$", fontsize=10, ha="center", va="center")
    save(fig, "fig6_fidelity_vs_information")


# ----------------------------------------------------------------------------------------------
def fig8():
    """QEC as a correlation filter (mechanism) and comparison of three strategies."""
    fig, ax = canvas(4.55)
    ax.text(0.1, 4.4, "(a) how syndrome measurement separates a collective kick from local noise",
            fontweight="bold", fontsize=7.6, va="center")

    def qubits(y, marked=None, tilt=False):
        for k in range(7):
            cx = 0.28 + 0.2 * k
            ax.add_patch(plt.Circle((cx, y), 0.07, fc=ORANGE if k == marked else SURF,
                                    ec=ORANGE if k == marked else INK2, lw=0.9, zorder=3))
            if tilt:
                ax.plot([cx, cx + 0.045], [y + 0.1, y + 0.2], color=BLUE, lw=1.3, zorder=3)

    ya, yb_ = 3.55, 2.45
    qubits(ya, tilt=True)
    ax.text(0.2, ya + 0.3, "signal: all qubits rotated by\n" + r"the same small angle $\epsilon$", fontsize=7.2,
            va="bottom", linespacing=1.3)
    qubits(yb_, marked=3)
    ax.text(0.2, yb_ + 0.16, "noise: one qubit suffers an error", fontsize=7.2, va="bottom")
    box(ax, 2.55, 2.55, 1.15, 0.9, "Syndrome\nmeasurement")
    arrow(ax, [(1.72, ya), (2.2, ya), (2.55, 3.25)])
    arrow(ax, [(1.72, yb_), (2.2, yb_), (2.55, 2.75)])
    outs = [
        (3.72, "no check fires", r"probability $1-\frac{7}{4}\epsilon^2$", r"logical phase $\frac{7}{4}\epsilon^3$", True),
        (3.0, "one check fires (signal)", r"probability $\frac{7}{4}\epsilon^2$",
         r"logical phase $3\epsilon$, opposite sign", True),
        (2.28, "one check fires (noise)", "corrected", "no logical phase", False),
    ]
    for yy, t, l1, l2, sig in outs:
        box(ax, 4.25, yy - 0.3, 2.45, 0.6, fc=BLUE_TINT if sig else NEUTRAL, ec=BLUE_EDGE if sig else AXIS)
        ax.text(4.37, yy + 0.19, t, fontsize=7.4, fontweight="bold", va="center")
        ax.text(4.37, yy - 0.01, l1, fontsize=7, color=INK2, va="center")
        ax.text(4.37, yy - 0.19, l2, fontsize=7, color=INK2, va="center")
        arrow(ax, [(3.7, 3.0), (3.95, 3.0), (3.95, yy), (4.25, yy)] if abs(yy - 3.0) > 0.01 else [(3.7, 3.0), (4.25, 3.0)])

    ax.text(0.1, 1.82, "(b) Fisher information per expected signal event, Steane code "
            r"($n=7$, $R/\gamma=0.5$, $\delta t\to0$)", fontweight="bold", fontsize=7.6, va="center")
    b = fig.add_axes([0.085, 0.1, 0.5, 0.265])
    eps = np.logspace(np.log10(0.004), np.log10(0.2), 300)
    n, ratio = 7, 0.5
    f_ram = np.full_like(eps, n * ratio / (4 * np.e))
    f_det = n**4 * eps**2 / 16
    f_log = np.full_like(eps, n / np.e)
    b.loglog(eps, f_log, color=BLUE)
    b.loglog(eps, f_ram, color=ORANGE)
    b.loglog(eps, f_det, color=AQUA)
    b.plot([0.036, 0.036], [1e-3, 20], color=MUTED, lw=0.7)
    b.text(0.039, 1.5e-3, r"$\epsilon=0.036$" + "\n(Ott et al.)", fontsize=6.6, color=INK2, va="bottom", linespacing=1.25)
    style_axes(b)
    b.set_xlim(eps[0], eps[-1])
    b.set_ylim(1e-3, 20)
    b.set_xticks([0.01, 0.1])
    b.set_xticklabels(["0.01", "0.1"])
    b.set_yticks([1e-2, 1e-1, 1, 10])
    b.set_yticklabels(["0.01", "0.1", "1", "10"])
    b.set_xlabel(r"kick angle $\epsilon$")
    b.set_ylabel(r"$F_{\mathrm{tot}}/RT$")
    xe = eps[-1]
    for yend, ylab, c, l1, l2 in [
        (f_det[-1], 9.0, AQUA, "error detection only", r"$n^4\epsilon^2/16$"),
        (f_log[-1], 0.9, BLUE, "logical sensing with QEC", r"$n/e$"),
        (f_ram[-1], 0.09, ORANGE, "Ramsey, no encoding", r"$nR/4e\gamma$"),
    ]:
        b.plot([xe * 1.06, xe * 1.5, xe * 1.9], [yend, ylab, ylab], color=c, lw=1.2, clip_on=False, solid_capstyle="butt")
        b.plot([xe], [yend], marker="o", ms=5, color=c, mec=SURF, mew=1.0, clip_on=False, zorder=6)
        b.text(xe * 2.1, ylab, l1, fontsize=7.4, va="bottom", ha="left")
        b.text(xe * 2.1, ylab, l2, fontsize=7.4, va="top", ha="left", color=INK2)
    save(fig, "fig8_correlation_filter")


# ----------------------------------------------------------------------------------------------
def fig7():
    """Two-tier decoding architecture."""
    fig, ax = canvas(3.2)
    box(ax, 0.15, 1.2, 1.5, 0.8, "Logical sensor", "code, signal, noise")
    box(ax, 2.65, 2.2, 1.9, 0.8, "Tier 1: fast decoder", "real time, approximate", fc=BLUE_TINT, ec=BLUE_EDGE)
    box(ax, 2.65, 0.2, 1.9, 0.8, "Tier 2: offline smoother", "accurate, uses the whole record",
        fc=BLUE_TINT, ec=BLUE_EDGE)
    box(ax, 4.95, 1.2, 1.78, 0.8, "Estimator", r"$\hat\theta=\sum_i x_iw_i\;/\;\lambda\sum_i w_i^2$", bsize=7.4)
    arrow(ax, [(1.65, 1.6), (4.95, 1.6)])
    ax.text(3.3, 1.66, r"readout $x$, one bit per shot", fontsize=7, color=INK2, ha="center", va="bottom")
    arrow(ax, [(1.25, 2.0), (1.25, 2.42), (2.65, 2.42)])
    ax.text(1.95, 2.36, "syndrome stream", fontsize=7, color=INK2, ha="center", va="top")
    arrow(ax, [(2.65, 2.82), (0.55, 2.82), (0.55, 2.0)])
    ax.text(1.6, 2.88, r"recovery pulses, delay $\tau_d$", fontsize=7, color=INK2, ha="center", va="bottom")
    arrow(ax, [(1.25, 1.2), (1.25, 0.6), (2.65, 0.6)])
    ax.text(1.95, 0.66, r"full record $s$", fontsize=7, color=INK2, ha="center", va="bottom")
    arrow(ax, [(4.55, 0.6), (5.95, 0.6), (5.95, 1.2)], color=BLUE, lw=2.0, head=11)
    ax.text(5.25, 0.66, r"weight $w(s)$", fontsize=7, color=INK2, ha="center", va="bottom")
    ax.text(4.65, 2.72, "mistakes here cost\ngain only", fontsize=7, color=INK2, va="center", linespacing=1.3)
    ax.text(4.65, 0.27, r"quality $=\mathrm{corr}^2(\hat w,w)$", fontsize=7, color=INK2, va="center")
    save(fig, "fig7_two_tier_decoding")


# ----------------------------------------------------------------------------------------------
def fig9():
    """Feature-sufficient subsystem code."""
    fig, ax = canvas(2.55)
    ax.add_patch(FancyBboxPatch((2.5, 0.2), 2.3, 2.15, boxstyle="round,pad=0,rounding_size=0.1",
                                fc=SURF, ec=AXIS, lw=0.9, zorder=1))
    ax.text(3.65, 2.17, r"code space $\mathcal{C}=\mathcal{H}_L\otimes\mathcal{H}_G$", fontsize=7.6, ha="center",
            va="center", color=INK2)
    box(ax, 2.7, 1.25, 1.9, 0.7, r"logical subsystem $\mathcal{H}_L$", "decoded and read out", fc=BLUE_TINT,
        ec=BLUE_EDGE, tsize=7.8)
    box(ax, 2.7, 0.35, 1.9, 0.7, r"gauge subsystem $\mathcal{H}_G$", "never decoded", tsize=7.8)
    ax.text(0.15, 1.6, r"feature generator $w\cdot G$", fontsize=7.6, va="center")
    arrow(ax, [(1.95, 1.6), (2.7, 1.6)], color=BLUE, lw=2.0, head=11)
    ax.text(0.15, 0.88, r"nuisance generators $v\cdot G$, $v\perp w$", fontsize=7.6, va="center")
    arrow(ax, [(2.38, 0.88), (2.7, 0.8)])
    ax.text(0.15, 0.52, r"noise $E_a^\dagger E_b$", fontsize=7.6, va="center")
    arrow(ax, [(1.15, 0.52), (2.7, 0.6)])
    arrow(ax, [(4.6, 1.6), (5.0, 1.6)], color=BLUE, lw=2.0, head=11)
    ax.text(5.08, 1.71, "depends on the parameters", fontsize=7.4, va="center")
    ax.text(5.08, 1.49, r"only through $f=w^{\mathsf{T}}\theta$", fontsize=7.4, va="center")
    arrow(ax, [(4.6, 0.7), (5.0, 0.7)])
    ax.text(5.08, 0.81, "absorbs nuisance", fontsize=7.4, va="center", color=INK2)
    ax.text(5.08, 0.59, "terms and noise", fontsize=7.4, va="center", color=INK2)
    save(fig, "fig9_feature_subsystem")


FIGS = dict(fig1=fig1, fig2=fig2, fig3=fig3, fig4=fig4, fig5=fig5, fig6=fig6, fig7=fig7, fig8=fig8, fig9=fig9)

if __name__ == "__main__":
    for name in (sys.argv[1:] or list(FIGS)):
        FIGS[name]()
