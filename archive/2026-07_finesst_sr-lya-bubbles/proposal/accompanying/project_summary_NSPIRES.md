# NSPIRES Project Summary (anonymized — pasted into the web cover page)

Rules: DAPR-compliant (no names, no institutions, no "my/our previous
work"); do NOT duplicate it inside the uploaded proposal PDF. ~4000
character limit in NSPIRES (verify the field limit when pasting).

---

The Epoch of Reionization (EoR) — the last major phase transition of the
Universe — is bracketed in time, but its morphology remains unmeasured:
we do not know the characteristic sizes of the ionized bubbles that grew
and merged around the first galaxies, or which sources drove that growth.
The bubble size distribution as a function of redshift is the key
observable separating competing reionization scenarios. The Lyman-alpha
emission line of z > 7 galaxies directly encodes this information: its
visibility, equivalent width, and velocity structure depend on the size
of the ionized region through which the photons escape. The obstacle is
that statistically large EoR samples exist almost exclusively at low
spectral resolution — the JWST/NIRSpec prism (R ~ 100) and, soon, the
Roman Space Telescope grism — where this diagnostic information is
smeared below the instrumental resolution.

This project will break that barrier using a recently demonstrated,
physics-informed deep-learning framework that super-resolves real
JWST/NIRSpec prism spectra by a factor of ~10 in resolving power, trained
on ~1,200 paired prism-grating observations from the public JADES survey,
with calibrated uncertainties and a built-in falsification test that
measures whether the model reads the data rather than reciting its
training prior. The proposed research will (1) validate which
Lyman-alpha diagnostics are recoverable from prism-resolution data,
via held-out paired observations and controlled mock experiments,
including a decisive comparison between super-resolve-then-infer and
direct low-resolution inference; (2) couple the validated inference to
neural posterior estimation trained on multiple independent
radiative-transfer simulations of patchy reionization, and apply it to
more than one hundred public JADES spectra to deliver the first
statistical measurement of the ionized bubble size distribution at
z = 7–9; and (3) adapt the framework to Roman grism spectroscopy —
where Lyman-alpha enters the bandpass at z > 7.2 — using public Roman
grism simulation products and an already-working end-to-end extraction
pipeline, producing completeness and recovery forecasts so the
measurement can be extended to the rare, luminous galaxies tracing the
largest bubbles as soon as Roman wide-area survey data become public.

The investigation uses NASA mission data exclusively: public JWST
archival spectroscopy from MAST and Roman preparation products from
IRSA. It directly supports the Astrophysics Division goals to probe the
origin of the Universe and the evolution of galaxies, delivers
open-source software, trained models, and value-added catalogs to the
community, and develops methodology — trustworthy machine-learning
spectral inference with built-in falsification — directly transferable
to Roman's survey-scale emission-line science and future missions.

---
(~2,500 characters — fits typical NSPIRES limits.)
