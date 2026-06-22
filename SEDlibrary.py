import pandas as pd
import matplotlib.pyplot as plt
import math

def SEDplt(file_path, source_name):
    rows = []

    with open(file_path, "r") as f:

        for line in f:

            line = line.strip()

            if line.startswith("#"):
                continue

            parts = line.split()

            rows.append([float(x) for x in parts[:6]])

    df = pd.DataFrame(rows)

    # REMOVE bad values before Log10
    df = df[df[0] > 0]   # frequency > 0
    df = df[df[2] > 0]   # flux > 0

    freq = df[0]
    flux = df[2]

    # Convert to Log scale
    log_freq = freq.apply(math.log10)
    log_flux = flux.apply(math.log10)

    plt.figure(figsize=(10,7))

    plt.scatter(log_freq, log_flux, s=8)

    plt.xlabel("Log Frequency (Hz)")
    plt.ylabel("Log νFν")
    plt.title(f"{source_name} SED")
    plt.grid(True)

    plt.xlim(7, 28)
    plt.ylim(-16, -7)

    plt.show()