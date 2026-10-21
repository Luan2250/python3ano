"""Gráfico de pizza: participação de cada canal de venda no faturamento.

Dados: dados/dados_pizza.csv (canal_venda, faturamento)
Saída: imagens/pizza.png
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PASTA_PROJETO = Path(__file__).resolve().parent.parent
ARQUIVO_CSV = PASTA_PROJETO / "dados" / "dados_pizza.csv"
ARQUIVO_IMAGEM = PASTA_PROJETO / "imagens" / "pizza.png"

try:
    df = pd.read_csv(ARQUIVO_CSV)
except FileNotFoundError:
    sys.exit(f"Arquivo não encontrado: {ARQUIVO_CSV}")


legenda = [
    f"{canal} — {valor:,.0f}".replace(",", ".")
    for canal, valor in zip(df["canal_venda"], df["faturamento"])
]

fig, ax = plt.subplots(figsize=(8, 7))

ax.pie(
    df["faturamento"],
    autopct="%1.1f%%",  
    startangle=90,
    colors=sns.color_palette("pastel", len(df)),
    wedgeprops={"edgecolor": "white"},
)
ax.axis("equal") 

ax.set_title("Faturamento por Canal de Venda", fontsize=14, fontweight="bold")
ax.legend(legenda, title="Canal — faturamento", loc="center left", bbox_to_anchor=(1, 0.5))

plt.tight_layout()
ARQUIVO_IMAGEM.parent.mkdir(exist_ok=True)
plt.savefig(ARQUIVO_IMAGEM, dpi=300, bbox_inches="tight")
print(f"Imagem salva em: {ARQUIVO_IMAGEM}")
plt.show()
