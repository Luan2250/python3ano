"""Gráfico de linhas: vendas diárias ao longo do tempo (jan-mar).

Dados: dados/dados_linhas.csv (data, vendas, loja)
Saída: imagens/linhas.png

Observação: cada data aparece uma única vez no arquivo (uma loja por dia).
Por isso a linha mostra a série diária completa, e a cor dos pontos indica
a loja do registro.
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PASTA_PROJETO = Path(__file__).resolve().parent.parent
ARQUIVO_CSV = PASTA_PROJETO / "dados" / "dados_linhas.csv"
ARQUIVO_IMAGEM = PASTA_PROJETO / "imagens" / "linhas.png"

try:
    df = pd.read_csv(ARQUIVO_CSV, parse_dates=["data"])
except FileNotFoundError:
    sys.exit(f"Arquivo não encontrado: {ARQUIVO_CSV}")

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(11, 6))

sns.lineplot(
    data=df,
    x="data",
    y="vendas",
    color="gray",
    linewidth=1.5,
    label="Vendas diárias",
    ax=ax,
)

sns.scatterplot(
    data=df,
    x="data",
    y="vendas",
    hue="loja",
    s=50,
    ax=ax,
)

ax.set_title("Evolução das Vendas Diárias", fontsize=14, fontweight="bold")
ax.set_xlabel("Data", fontsize=11)
ax.set_ylabel("Vendas", fontsize=11)
ax.legend(title="Legenda", frameon=True)
fig.autofmt_xdate() 

plt.tight_layout()
ARQUIVO_IMAGEM.parent.mkdir(exist_ok=True)
plt.savefig(ARQUIVO_IMAGEM, dpi=300, bbox_inches="tight")
print(f"Imagem salva em: {ARQUIVO_IMAGEM}")
plt.show()
