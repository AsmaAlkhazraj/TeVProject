import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def SEDplt(file_path, source_name):

    rows = []

    with open(file_path, "r") as f:

        for line in f:

            line = line.strip()

            if line.startswith("#") or line == "":
                continue

            # Remove comments such as "; UPPER LIMIT"
            line = line.split(";")[0]

            parts = line.split()

            if len(parts) >= 6:
                rows.append([float(x) for x in parts[:6]])

    df = pd.DataFrame(rows)

    # Keep only positive values
    df = df[(df[0] > 0) & (df[2] > 0)]

    # Columns
    freq = df[0]          # Frequency (Hz)
    flux = df[2]          # νFν
    flux_err = df[3]      # νFν error

    # Frequency -> Energy conversion
    h = 6.62607015e-34          # Planck constant (J s)
    eV = 1.602176634e-19        # 1 eV in Joules

    energy = (h * freq) / eV

    # Log quantities
    log_energy = np.log10(energy)
    log_freq = np.log10(freq)
    log_flux = np.log10(flux)

    # Error propagation in log space
    log_flux_err = np.where(
        flux_err > 0,
        flux_err / (flux * np.log(10)),
        0
    )

    # Plot
    fig, ax = plt.subplots(figsize=(10, 7))

    ax.errorbar(
        log_energy,
        log_flux,
        yerr=log_flux_err,
        fmt='o',
        markersize=3,
        color='blue',
        markerfacecolor='blue',
        markeredgecolor='blue',
        ecolor='blue',
        elinewidth=1,
        capsize=2,
        linestyle='none',
        label=source_name
    )

    ax.set_xlabel("Energy (eV)")
    ax.set_ylabel(r"$\nu F_{\nu}$ (erg cm$^{-2}$ s$^{-1}$)")
    ax.set_title(f"{source_name} SED")

    ax.grid(True)

    # Upper x-axis : Frequency
    # Lower x-axis : Energy
    top_ax = ax.twiny()

    top_ax.set_xlim(ax.get_xlim())

    energy_ticks = ax.get_xticks()
    freq_ticks = (10**energy_ticks * eV) / h

    top_ax.set_xticks(energy_ticks)
    top_ax.set_xticklabels([f"{np.log10(f):.1f}" for f in freq_ticks])

    top_ax.set_xlabel("Frequency (Hz)")

    ax.legend()

    plt.show()