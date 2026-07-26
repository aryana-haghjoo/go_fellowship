# Figure 1 — step-by-step instructions

Goal: a single two-panel figure (full text width, target height ≤ 7 cm
total so the S/T/M stays at 6 pages) that makes the science case visually:
**(a)** the SR framework works on real data near Lyα; **(b)** bubble size
imprints a measurable signature that prism resolution smears out.

DAPR rules for this figure: no names/institutions in the plot or caption
(JADES/JWST/NIRSpec are fine); no logos; don't reference "our paper" in
the caption — cite as [15].

## Panel (a) — Real JADES pair + SR output, zoomed on Lyα

Repo: `~/Documents/GitHub/super_resolution`

1. Find test-set objects at z > 5.8 (so Lyα at (1+z)·1216 Å > 8300 Å is
   comfortably inside both the prism and stitched-grating coverage; recall
   the HR grid starts at 1 µm so you need z ≳ 7.2 for Lyα on the HR grid —
   **if the HR grid cuts Lyα, fall back to a z≈7.3–7.5 object or center
   the panel on the Lyα-break + [OIII]/Hβ region instead and let panel (b)
   carry the Lyα message**):
   - Load the split file in `train/splits/split_<HASH>.npz`, take test
     indices, filter `redshift` in the dataset npz for z in [7.2, 8.0].
2. Run inference on the chosen indices:
   ```bash
   cd train/sr2_best
   python infer_sr2.py --idx <i1> <i2> <i3> --save lya_candidates.npz
   ```
3. Plot per candidate: LR prism input (interpolated grid), grating truth
   (HR), `sr2_mean` with ±1σ band (`sr2_sigma`), x-axis in observed µm
   zoomed to (1+z)·1216 Å ± 400 Å rest. Pick the object where SR visibly
   recovers the line/break that the prism smears.
4. Style: three curves (LR grey, HR black thin, SR colored + band),
   labeled axes (F_λ vs observed wavelength), z annotated as "z = 7.4"
   (no object ID needed; IDs are fine too — they're catalog numbers, not
   identities).

## Panel (b) — Simulated Lyα profiles vs bubble size, at two resolutions

Repo: `~/Documents/GitHub/Lyman_alpha`

1. Take one median intrinsic Lyα template from the z=4–5.5 template set
   (`notebooks/task2_jades_lya_templates.ipynb` output, 325 templates).
2. Generate 4 analytic transmission curves for bubble radii
   R_b = 0.1, 0.5, 1, 3 pMpc at z = 8: use the Miralda-Escudé (1998)
   damping-wing formula with x_HI = 0.5 outside the bubble (this is a
   ~20-line function; alternatively pull 4 sightlines with those measured
   bubble sizes from the sim transmission files in
   `data/for_aryana/late_end_early_start/Lya_transmission/`).
3. Multiply template × transmission → "emergent" profiles at R = 1000.
4. Convolve each with the prism LSF at ~1.1 µm (R ≈ 50; Gaussian with
   σ = λ/(2.355·R)) → "prism view".
5. Plot: left sub-axis emergent profiles at R=1000 (4 colors by R_b with
   a colorbar or legend "R_b [pMpc]"), right sub-axis the same after prism
   convolution — visually: distinct profiles collapse into
   near-identical smooth bumps. That contrast IS the proposal.

## Assembly

- `fig, axs = plt.subplots(1, 3, figsize=(13, 3.2))` — (a) one axis,
  (b) two axes; or 1×2 with (b) as overplot pairs. Export PDF:
  `fig.savefig("figure1.pdf", bbox_inches="tight")`.
- Put `figure1.pdf` in `proposal/anonymized/`, replace the `\fbox`
  placeholder in `main.tex` with
  `\includegraphics[width=\textwidth]{figure1.pdf}`, recompile, and
  check the S/T/M still ends on page 6 (references start p7).
- Caption draft (anonymized, edit freely):
  > **Figure 1.** *(a)* A JADES galaxy at z = 7.4: the NIRSpec prism
  > spectrum (grey), the medium-resolution grating reference (black), and
  > the super-resolved output of the framework [15] with 1σ uncertainty
  > (color). *(b)* A fixed intrinsic Lyα profile transmitted through
  > ionized bubbles of R_b = 0.1–3 pMpc at z = 8, shown at R = 1000
  > (left) and convolved to prism resolution (right): the bubble-size
  > signature that is unresolved in the prism data is the information this
  > program recovers and exploits.
