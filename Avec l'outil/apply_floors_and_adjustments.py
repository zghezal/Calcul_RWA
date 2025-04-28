import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def apply_floors_and_adjustments(df: pd.DataFrame) -> pd.DataFrame:
    """Applique les floors et ajustements sur le portefeuille."""
    # Floors et ajustements
    #bloc 4
    df['PD_adj'] = df[['PD','floor_PD']].max(axis=1)
    #bloc 5
    df['LGD_adj'] = df[['LGD','floor_LGD']].max(axis=1)
    #bloc 6
    df['LGD_adj'] *= df['SME_reduction_factor']
    return df
