import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def calculate_rwa(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # IRB Foundation simplifiée
    #bloc 7
    df['K'] = df.apply(lambda r: r['LGD_adj'] * norm.ppf(r['PD_adj']) * np.sqrt(r['M']), axis=1)
    #bloc 8
    df['RWA'] = 12.5 * df['EAD_adj'] * df['K']
    return df
