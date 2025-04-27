#!/usr/bin/env python3

"""
Script IRB RWA à partir d'un fichier Excel.
Usage:
  python rwa_irb_excel.py <fichier_excel>

Le fichier Excel doit contenir deux onglets :
  - portefeuille : colonnes ['ID','EAD','PD','LGD','M','CA','AVC','risk_grade']
  - precision    : colonnes ['risk_grade','floor_PD','floor_LGD','SME_reduction_factor','AVC']

Le script :
 1. Charge les deux feuilles depuis l'Excel
 2. Applique les planchers et ajustements
 3. Calcule K et RWA selon IRB Foundation simplifiée
 4. Trace la distribution cumulée des RWA
 5. Sauvegarde les résultats dans une nouvelle feuille 'rwa'
"""
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


def load_excel_data(path: str, sheet_portf: str = 'portefeuille', sheet_prec: str = 'precision') -> tuple[pd.DataFrame, pd.DataFrame]:
    """Lit les feuilles 'portefeuille' et 'precision' depuis l'Excel."""
    df_port = pd.read_excel(path, sheet_name=sheet_portf)
    df_prec = pd.read_excel(path, sheet_name=sheet_prec)
    return df_port, df_prec


def enrich_portfolio(df: pd.DataFrame, prec: pd.DataFrame) -> pd.DataFrame:
    df = df.merge(prec, on='risk_grade', how='left')
    return df

def apply_floors_and_adjustments(df: pd.DataFrame) -> pd.DataFrame:
    # Floors et ajustements
    df['PD_adj'] = df[['PD','floor_PD']].max(axis=1)
    df['LGD_adj'] = df[['LGD','floor_LGD']].max(axis=1)
    df['LGD_adj'] *= df['SME_reduction_factor']
    df['EAD_adj'] = df['EAD'] - df['AVC']
    return df


def calculate_rwa(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # IRB Foundation simplifiée
    df['K'] = df.apply(lambda r: r['LGD_adj'] * norm.ppf(r['PD_adj']) * np.sqrt(r['M']), axis=1)
    df['RWA'] = 12.5 * df['EAD_adj'] * df['K']
    return df


def plot_cumulative_rwa(df: pd.DataFrame) -> None:
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


def main(excel_path: str):
    # Chargement
    df_port, df_prec = load_excel_data(excel_path)
    # Enrichissement du portefeuille
    df_port = enrich_portfolio(df_port, df_prec)
    # Calcul des ajustements
    df_adj = apply_floors_and_adjustments(df_port)
    # Calcul des RWA
    df_rwa = calculate_rwa(df_adj)
    # Tracé
    plot_cumulative_rwa(df_rwa)
    # Sauvegarde résultats dans 'rwa'
    with pd.ExcelWriter(excel_path, mode='a', if_sheet_exists='replace') as writer:
        df_rwa.to_excel(writer, sheet_name='rwa', index=False)
    print(f"RWA calculées et enregistrées dans la feuille 'rwa' de {excel_path}")


if __name__ == '__main__':

    main("example_data.xlsx")