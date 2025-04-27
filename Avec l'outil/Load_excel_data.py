import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# encadre 1
def load_excel_data(path: str, sheet_portf: str = 'portefeuille', sheet_prec: str = 'precision') -> tuple[pd.DataFrame, pd.DataFrame]:
    """Lit les feuilles 'portefeuille' et 'precision' depuis l'Excel."""
    ### Bloc 1
    df_port = pd.read_excel(path, sheet_name=sheet_portf)

    ### Bloc 2
    df_prec = pd.read_excel(path, sheet_name=sheet_prec)
    
    return df_port, df_prec
