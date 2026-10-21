"""Gráfico de dispersão: altura x peso, separado por sexo.

Dados: dados/dados_dispersao.csv (altura_cm, peso_kg, sexo)
Saída: imagens/dispersao.png
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PASTA_PROJETO = Path(__file__).resolve().parent.parent
ARQUIVO_CSV = PASTA_PROJETO / "dados" / "dados_dispersao.csv"
ARQUIVO_IMAGEM = PASTA_PROJETO / "imagens" / "dispersao.png"

try:
    df = pd.read_csv(ARQUIVO_CSV)
except FileNotFoundError:
    sys.exit(f"Arquivo não encontrado: {ARQUIVO_CSV}")

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(9, 6))

sns.scatterplot(
    data=df,
    x="altura_cm",
    y="peso_kg",
    hue="sexo",
    style="sexo",
    s=70,       
    alpha=0.8,  
    ax=ax,
)

ax.set_title("Relação entre Altura e Peso", fontsize=14, fontweight="bold")
ax.set_xlabel("Altura (cm)", fontsize=11)
ax.set_ylabel("Peso (kg)", fontsize=11)
ax.legend(title="Sexo", frameon=True)

plt.tight_layout()
ARQUIVO_IMAGEM.parent.mkdir(exist_ok=True)
plt.savefig(ARQUIVO_IMAGEM, dpi=300, bbox_inches="tight")
print(f"Imagem salva em: {ARQUIVO_IMAGEM}")
plt.show()
