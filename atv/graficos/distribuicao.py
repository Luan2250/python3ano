"""Gráfico de distribuição: idade dos clientes (histograma + curva KDE).

Dados: dados/dados_distribuicao.csv (cliente_id, idade)
Saída: imagens/distribuicao.png
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PASTA_PROJETO = Path(__file__).resolve().parent.parent
ARQUIVO_CSV = PASTA_PROJETO / "dados" / "dados_distribuicao.csv"
ARQUIVO_IMAGEM = PASTA_PROJETO / "imagens" / "distribuicao.png"

try:
    df = pd.read_csv(ARQUIVO_CSV)
except FileNotFoundError:
    sys.exit(f"Arquivo não encontrado: {ARQUIVO_CSV}")

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(9, 6))

sns.histplot(
    data=df,
    x="idade",
    bins=15,    
    kde=True,   
    color="#4c72b0",
    ax=ax,
)

ax.set_title("Distribuição da Idade dos Clientes", fontsize=14, fontweight="bold")
ax.set_xlabel("Idade (anos)", fontsize=11)
ax.set_ylabel("Número de clientes", fontsize=11)

plt.tight_layout()
ARQUIVO_IMAGEM.parent.mkdir(exist_ok=True)
plt.savefig(ARQUIVO_IMAGEM, dpi=300, bbox_inches="tight")
print(f"Imagem salva em: {ARQUIVO_IMAGEM}")
plt.show()
