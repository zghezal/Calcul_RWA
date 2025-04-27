import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from openpyxl import load_workbook

# encadre 2 : MERGE
def enrich_portfolio(df: pd.DataFrame, prec: pd.DataFrame) -> pd.DataFrame:
    """Enrichit le portefeuille avec les données de la feuille 'precision'."""
    ### Bloc 3
    df = df.merge(prec, on='risk_grade', how='left')
    return df