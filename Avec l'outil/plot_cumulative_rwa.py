import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


def plot_cumulative_rwa(df: pd.DataFrame) -> None:

    #bloc 9
    rwa = df['RWA'].sort_values().values
    cum = np.cumsum(rwa) / rwa.sum()
    plt.figure(figsize=(8,5))
    plt.step(rwa, cum, where='post')
    plt.xlabel('RWA')
    plt.ylabel('Distribution cumulée')
    plt.title('Distribution cumulée des RWA IRB')
    plt.grid(True)
    plt.tight_layout()
    plt.show()