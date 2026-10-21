"""Gráfico de barras: vendas médias por categoria e região.

Dados: dados/dados_barras.csv (categoria, regiao, vendas_medias)
Saída: imagens/barras.png

Os valores já vêm prontos (uma linha para cada categoria + região),
então não é preciso calcular soma nem média.
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PASTA_PROJETO = Path(__file__).resolve().parent.parent
ARQUIVO_CSV = PASTA_PROJETO / "dados" / "dados_barras.csv"
ARQUIVO_IMAGEM = PASTA_PROJETO / "imagens" / "barras.png"

# 1. Ler os dados
try:
    df = pd.read_csv(ARQUIVO_CSV)
except FileNotFoundError:
    sys.exit(f"Arquivo não encontrado: {ARQUIVO_CSV}")

# 2. Construir o gráfico
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(11, 6))

sns.barplot(
    data=df,
    x="categoria",
    y="vendas_medias",
    hue="regiao",     
    palette="Set2",
    errorbar=None,    
    ax=ax,
)

ax.set_title("Vendas Médias por Categoria e Região", fontsize=14, fontweight="bold")
ax.set_xlabel("Categoria", fontsize=11)
ax.set_ylabel("Vendas médias", fontsize=11)
ax.legend(title="Região", frameon=True)

plt.tight_layout()
ARQUIVO_IMAGEM.parent.mkdir(exist_ok=True)
plt.savefig(ARQUIVO_IMAGEM, dpi=300, bbox_inches="tight")
print(f"Imagem salva em: {ARQUIVO_IMAGEM}")
plt.show()
