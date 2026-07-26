#!/usr/bin/env python3
"""
Figure 1 of the FINESST S/T/M (see FIGURE1_INSTRUCTIONS.md).

(a) Real JADES prism/grating pair at z=7.43 (dataset idx 113, test split)
    + SR2 output with 1-sigma band, zoomed on Hbeta + [OIII].
    Input: data/lya_candidates.npz, produced with
      super_resolution/train/sr2_best/infer_sr2.py --idx 345 1172 204 808 113 1079 717
(b) Median JADES z=4-5.5 LAE template x Miralda-Escude (1998) damping wing
    for bubbles R_b = 0.1, 0.5, 1, 3 pMpc at z=8 (x_HI=0.5 outside bubble,
    neutral IGM down to z=6), shown at R=1000 and convolved to prism R~50.
    Input: data/median_template.npz, built with
      Lyman_alpha/scripts/task3_mock_lya_lines/prepare_mock_dataset.py helpers
      (325 templates; the intrinsic profile is the peak-normalised median of
      the 47 clear LAEs, lightly smoothed).

Output: ../anonymized/figure1.pdf
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "anonymized" / "figure1.pdf"

LYA = 1215.67  # A
Z_SRC = 8.0    # panel (b) source redshift
Z_END = 6.0    # end of reionization
X_HI = 0.5     # neutral fraction outside the bubble
RADII = [0.1, 0.5, 1.0, 3.0]  # pMpc

# Okabe-Ito vermillion for the SR curve; sequential blues for bubble sizes
C_SR = "#D55E00"
C_LR = "0.62"
C_HR = "black"


# ── Miralda-Escude (1998) damping wing ──────────────────────────────────────
def me_I(x):
    x = np.clip(x, 1e-12, 1 - 1e-9)
    sx = np.sqrt(x)
    return (x**4.5 / (1 - x) + 9 / 7 * x**3.5 + 9 / 5 * x**2.5
            + 3 * x**1.5 + 9 * sx - 4.5 * np.log((1 + sx) / (1 - sx)))


def tau_gp(z):
    return 7.16e5 * ((1 + z) / 10.0) ** 1.5


def hubble(z, h0=67.7, om=0.31):  # km/s/Mpc
    return h0 * np.sqrt(om * (1 + z) ** 3 + (1 - om))


def damping_wing_T(wav_rest, z_s, r_b_pmpc, x_hi, z_end):
    """IGM transmission for a source inside an ionized bubble of proper
    radius r_b; uniform neutral (x_hi) IGM from the bubble edge to z_end.
    Blueward of the systemic Lya resonance: saturated (T = 0)."""
    r_alpha = 2.02e-8  # damping const / (4 pi nu_alpha)
    c = 2.998e5        # km/s
    z_b = z_s - r_b_pmpc * hubble(z_s) * (1 + z_s) / c
    one_pz_lam = (wav_rest / LYA) * (1 + z_s)
    T = np.zeros_like(wav_rest, dtype=float)
    red = wav_rest > LYA
    x_b = (1 + z_b) / one_pz_lam[red]
    x_e = (1 + z_end) / one_pz_lam[red]
    tau = (x_hi * r_alpha * tau_gp(z_s) / np.pi
           * (one_pz_lam[red] / (1 + z_s)) ** 1.5
           * (me_I(x_b) - me_I(x_e)))
    T[red] = np.exp(-tau)
    return T


def gauss_convolve(y, sigma_px):
    n = max(int(6 * sigma_px) | 1, 3)
    xk = np.arange(n) - n // 2
    k = np.exp(-0.5 * (xk / sigma_px) ** 2)
    return np.convolve(y, k / k.sum(), mode="same")


# ── style ────────────────────────────────────────────────────────────────────
# the figure is included at \textwidth (~50% of its 13 in draw width),
# so all sizes are ~2x their printed size
plt.rcParams.update({
    "font.size": 14,
    "axes.titlesize": 15,
    "axes.labelsize": 15,
    "xtick.labelsize": 13,
    "ytick.labelsize": 13,
    "legend.fontsize": 12.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 1.1,
    "xtick.major.width": 1.1,
    "ytick.major.width": 1.1,
})

fig, axs = plt.subplots(
    1, 3, figsize=(13, 3.3),
    gridspec_kw={"width_ratios": [1.25, 1, 1], "wspace": 0.13},
)
ax_a, ax_b1, ax_b2 = axs

# ── panel (a): real JADES pair + SR, zoomed on Hbeta + [OIII] ────────────────
r = np.load(HERE / "data" / "lya_candidates.npz")
i = int(np.where(r["indices"] == 113)[0][0])
z = float(r["z_true"][i])
w = r["wave_um"]
lo, hi = 3.95, 4.36
m = (w >= lo) & (w <= hi)

ax_a.plot(w[m], r["x_high"][i][m], color=C_HR, lw=0.9, alpha=0.85,
          label="grating reference", zorder=2)
ax_a.plot(w[m], r["x_low"][i][m], color=C_LR, lw=3.2,
          label="prism input", zorder=3)
ax_a.plot(w[m], r["sr2_mean"][i][m], color=C_SR, lw=2.2,
          label=r"super-resolved $\pm1\sigma$", zorder=4)
ax_a.fill_between(
    w[m],
    (r["sr2_mean"][i] - r["sr2_sigma"][i])[m],
    (r["sr2_mean"][i] + r["sr2_sigma"][i])[m],
    color=C_SR, alpha=0.22, lw=0, zorder=1,
)
for rest, name, dx in [(0.486135, r"H$\beta$", 0),
                       (0.495890, "", 0),
                       (0.500680, r"[O III]$\lambda\lambda$4959,5007", 0.004)]:
    lam = rest * (1 + z)
    ax_a.axvline(lam, color="0.75", ls=":", lw=1.1, zorder=0)
    if name:
        ax_a.text(lam + dx, 6.75, name, ha="center", va="top",
                  fontsize=12, color="0.35")
ax_a.text(0.03, 0.955, f"$z = {z:.2f}$", transform=ax_a.transAxes,
          ha="left", va="top", fontsize=15)
ax_a.legend(loc="upper left", bbox_to_anchor=(0.015, 0.90), frameon=False,
            handlelength=1.6, borderpad=0.2, labelspacing=0.35)
ax_a.set_xlim(lo, hi)
ax_a.set_ylim(-1.7, 7.0)
ax_a.set_xlabel(r"observed wavelength [$\mu$m]")
ax_a.set_ylabel(r"$F_\lambda$ (normalized)")

# ── panel (b): Lya profile vs bubble size at two resolutions ─────────────────
d = np.load(HERE / "data" / "median_template.npz")
wav, tpl = d["wav"].astype(float), d["templates"]
lm = (wav > 1205) & (wav < 1235)
peaks = tpl[:, lm].max(axis=1)
sel = peaks > 3.0
stack = np.median(tpl[sel] / peaks[sel, None], axis=0)
cont = np.median(stack[(wav > 1260) & (wav < 1310)])
dlam = np.diff(wav).mean()
intrinsic = gauss_convolve(stack / cont, 3.0 / dlam)  # light smoothing

sig_hi = (LYA / 1000.0) / 2.355 / dlam  # R = 1000
sig_lo = (LYA / 50.0) / 2.355 / dlam    # prism R ~ 50 at 1.1 um

wobs = wav * (1 + Z_SRC) / 1e4
colors = plt.cm.Blues(np.linspace(0.38, 0.95, len(RADII)))
for rb, c in zip(RADII, colors):
    T = damping_wing_T(wav, Z_SRC, rb, X_HI, Z_END)
    em = intrinsic * T
    ax_b1.plot(wobs, gauss_convolve(em, sig_hi), color=c, lw=2.2,
               label=f"{rb:g}")
    ax_b2.plot(wobs, gauss_convolve(em, sig_lo), color=c, lw=2.2)

lya_obs = LYA * (1 + Z_SRC) / 1e4
for ax, title in [(ax_b1, r"emergent, $R = 1000$"),
                  (ax_b2, r"prism view, $R \approx 50$")]:
    ax.axvline(lya_obs, color="0.75", ls=":", lw=1.1, zorder=0)
    ax.set_xlim(1.076, 1.152)
    ax.set_ylim(-0.15, 4.9)
    ax.set_title(title, pad=3)
    ax.set_xlabel(r"observed wavelength [$\mu$m]")
ax_b1.text(lya_obs - 0.0015, 4.75, r"Ly$\alpha$", ha="right", va="top",
           fontsize=12, color="0.35")
ax_b1.legend(title=r"$R_b$ [pMpc]", loc="upper right", frameon=False,
             handlelength=1.6, borderpad=0.2, labelspacing=0.3,
             title_fontsize=12.5)
ax_b1.set_ylabel(r"$F_\lambda\, /\, F_{\rm cont}$")
ax_b2.tick_params(labelleft=False)

# panel letters
for ax, letter in [(ax_a, "(a)"), (ax_b1, "(b)")]:
    ax.text(-0.02, 1.06, letter, transform=ax.transAxes,
            ha="right", va="bottom", fontsize=17, fontweight="bold")

fig.savefig(OUT, bbox_inches="tight")
print(f"saved -> {OUT}")
