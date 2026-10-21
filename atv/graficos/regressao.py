"""Gráfico de regressão: renda mensal x gasto mensal.

Dados: dados/dados_regressao.csv (renda_mensal, gasto_mensal)
Saída: imagens/regressao.png
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PASTA_PROJETO = Path(__file__).resolve().parent.parent
ARQUIVO_CSV = PASTA_PROJETO / "dados" / "dados_regressao.csv"
ARQUIVO_IMAGEM = PASTA_PROJETO / "imagens" / "regressao.png"

try:
    df = pd.read_csv(ARQUIVO_CSV)
except FileNotFoundError:
    sys.exit(f"Arquivo não encontrado: {ARQUIVO_CSV}")

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(9, 6))

sns.regplot(
    data=df,
    x="renda_mensal",
    y="gasto_mensal",
    scatter_kws={"alpha": 0.6, "s": 50},   
    line_kws={"color": "red", "linewidth": 2},  
    ax=ax,
)

ax.set_title("Regressão: Renda Mensal x Gasto Mensal", fontsize=14, fontweight="bold")
ax.set_xlabel("Renda mensal", fontsize=11)
ax.set_ylabel("Gasto mensal", fontsize=11)

plt.tight_layout()
ARQUIVO_IMAGEM.parent.mkdir(exist_ok=True)
plt.savefig(ARQUIVO_IMAGEM, dpi=300, bbox_inches="tight")
print(f"Imagem salva em: {ARQUIVO_IMAGEM}")
plt.show()
