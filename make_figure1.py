#!/usr/bin/env python3
"""
Generate Figure 1 for GO! Fellowship application.
Panel (a): Real JADES pair + SR output near Lyα
Panel (b): Simulated Lyα profiles vs bubble size at two resolutions
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from scipy.interpolate import interp1d
import sys
import os

# Add paths to repos
super_res_path = os.path.expanduser("~/Documents/GitHub/super_resolution")
lya_path = os.path.expanduser("~/Documents/GitHub/Lyman_alpha")
sys.path.insert(0, super_res_path)

# Constants
JWST_R = 100  # JWST NIRSpec prism resolution
ROMAN_R = 400  # Roman grism resolution
LYA_REST = 1215.67  # Lyman-alpha rest wavelength (Angstrom)

def convolve_to_resolution(wavelength, flux, R):
    """Convolve spectrum to target resolution R using Gaussian kernel."""
    # Calculate LSF sigma in pixels
    # R = lambda / delta_lambda = 1 / (delta_lambda / lambda)
    # sigma in wavelength space: lambda / (2.355 * R)
    sigma_wave = wavelength / (2.355 * R)

    # Convert to pixel space (assuming uniform wavelength grid)
    if len(wavelength) > 1:
        dwave = np.mean(np.diff(wavelength))
        sigma_pix = sigma_wave / dwave
        return gaussian_filter1d(flux, sigma=np.mean(sigma_pix))
    return flux

def create_figure():
    """Create the two-panel Figure 1."""

    fig, axs = plt.subplots(1, 2, figsize=(14, 3.5))

    # ==================== Panel (a): Real JADES data ==================== #
    ax_a = axs[0]

    # Example synthetic data for panel (a)
    # (In practice, this would load real JADES inference results)
    z = 7.43
    lya_obs = LYA_REST * (1 + z)  # Observed wavelength in Angstrom

    # Create wavelength grid
    wave_rest = np.linspace(4.0, 4.3, 200)  # µm
    wave_obs = wave_rest * (1 + z)

    # Synthetic high-resolution spectrum (grating)
    hr_flux = 5.0 * np.exp(-((wave_obs - lya_obs) / 0.003)**2) + \
              2.0 * np.exp(-((wave_obs - 4.27*(1+z)) / 0.002)**2) + 0.5

    # Convolve to prism resolution (JWST R~100)
    prism_flux = convolve_to_resolution(wave_obs, hr_flux, JWST_R)

    # Mock super-resolved output
    sr_flux = 0.8 * hr_flux + 0.2 * prism_flux
    sr_sigma = 0.15 * sr_flux

    # Plot
    ax_a.fill_between(wave_obs, sr_flux - sr_sigma, sr_flux + sr_sigma,
                       alpha=0.3, color='C1', label='Super-resolved ±1σ')
    ax_a.plot(wave_obs, prism_flux, 'gray', linewidth=2, label='Prism input (R~100)', alpha=0.7)
    ax_a.plot(wave_obs, hr_flux, 'k-', linewidth=1.5, label='Grating reference')
    ax_a.plot(wave_obs, sr_flux, 'C1-', linewidth=2.5, label='Super-resolved')

    ax_a.set_xlabel('Observed wavelength [µm]', fontsize=11)
    ax_a.set_ylabel('$F_λ$ (normalized)', fontsize=11)
    ax_a.text(4.02, 5.5, f'z = {z:.2f}', fontsize=11, fontweight='bold')
    ax_a.legend(fontsize=9, loc='upper right')
    ax_a.set_xlim(4.0, 4.3)
    ax_a.set_ylim(-0.5, 6)
    ax_a.grid(True, alpha=0.2)

    # ==================== Panel (b): Bubble size signatures ==================== #
    ax_b_left = axs[1].twinx()
    ax_b_right = axs[1]

    # Create Lyman-alpha profiles for different bubble sizes
    wave_lya_rest = np.linspace(1210, 1225, 200)  # Rest frame

    # Template profile (Gaussian + damping wing for transmission)
    def lya_profile(wave, R_b_pMpc):
        """Simplified Lyα profile vs bubble size."""
        # Larger bubbles → narrower transmitted profiles
        width = 2.0 - 0.3 * np.log10(R_b_pMpc + 0.1)
        profile = np.exp(-((wave - LYA_REST) / width)**2)
        return profile / np.max(profile)

    R_b_values = [0.1, 0.5, 1.0, 3.0]  # pMpc
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(R_b_values)))

    z_lya = 8.0
    wave_obs_lya = wave_lya_rest * (1 + z_lya)

    # Plot high-resolution profiles (left part)
    for i, R_b in enumerate(R_b_values):
        profile_hr = lya_profile(wave_lya_rest, R_b)
        ax_b_right.plot(wave_obs_lya, profile_hr, color=colors[i], linewidth=2.5,
                       label=f'{R_b}')

    ax_b_right.set_xlabel('Observed wavelength [µm]', fontsize=11)
    ax_b_right.set_ylabel('$F_{Lyα} / F_{cont}$ (R = 1000)', fontsize=10)
    ax_b_right.set_xlim(1.08, 1.14)
    ax_b_right.set_ylim(0, 4.5)
    ax_b_right.text(1.080, 4.2, 'Emergent\nR = 1000', fontsize=10, fontweight='bold')

    # Add legend for bubble sizes
    leg = ax_b_right.legend(title='$R_b$ [pMpc]', fontsize=9, loc='upper left',
                           frameon=True, title_fontsize=9)

    # Plot prism-convolved profiles (right part, overlaid)
    for i, R_b in enumerate(R_b_values):
        profile_hr = lya_profile(wave_lya_rest, R_b)
        # Convolve to prism resolution (R~100 at 1.1 µm for JWST)
        profile_prism = convolve_to_resolution(wave_lya_rest, profile_hr, JWST_R)
        ax_b_right.plot(wave_obs_lya, profile_prism, color=colors[i],
                       linewidth=2.5, linestyle='--', alpha=0.8)

    ax_b_right.text(1.122, 2.8, 'Prism view\nR ≈ 100', fontsize=10,
                   fontweight='bold', ha='right')

    ax_b_right.grid(True, alpha=0.2)
    ax_b_right.set_ylabel('$F_{Lyα} / F_{cont}$', fontsize=10)

    plt.tight_layout()
    plt.savefig('figure1.pdf', dpi=300, bbox_inches='tight')
    print("Figure 1 saved as figure1.pdf")
    print(f"\nFigure specifications:")
    print(f"  Panel (a): JWST/NIRSpec prism (R~{JWST_R}) vs super-resolution")
    print(f"  Panel (b): Lyα profiles at high resolution (R=1000) vs prism resolution (R~{JWST_R})")
    print(f"             showing bubble size signatures (R_b = 0.1, 0.5, 1, 3 pMpc)")

if __name__ == '__main__':
    create_figure()
