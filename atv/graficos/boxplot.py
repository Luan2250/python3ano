"""Diagrama de caixa (boxplot): salários por departamento.

Dados: dados/dados_boxplot.csv (departamento, salario)
Saída: imagens/boxplot.png

Os valores atípicos (outliers) NÃO são removidos: aparecem como pontos
fora das caixas.
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PASTA_PROJETO = Path(__file__).resolve().parent.parent
ARQUIVO_CSV = PASTA_PROJETO / "dados" / "dados_boxplot.csv"
ARQUIVO_IMAGEM = PASTA_PROJETO / "imagens" / "boxplot.png"

try:
    df = pd.read_csv(ARQUIVO_CSV)
except FileNotFoundError:
    sys.exit(f"Arquivo não encontrado: {ARQUIVO_CSV}")

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(9, 6))

sns.boxplot(
    data=df,
    x="departamento",
    y="salario",
    hue="departamento",   
    palette="Pastel1",
    legend=False,        
    ax=ax,
)

ax.set_title("Distribuição de Salários por Departamento", fontsize=14, fontweight="bold")
ax.set_xlabel("Departamento", fontsize=11)
ax.set_ylabel("Salário", fontsize=11)

plt.tight_layout()
ARQUIVO_IMAGEM.parent.mkdir(exist_ok=True)
plt.savefig(ARQUIVO_IMAGEM, dpi=300, bbox_inches="tight")
print(f"Imagem salva em: {ARQUIVO_IMAGEM}")
plt.show()
