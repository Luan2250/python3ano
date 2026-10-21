"""Mapa de calor: movimento de clientes por dia da semana e horário.

Dados: dados/dados_heatmap.csv (dia_semana, horario, movimento_clientes)
Saída: imagens/heatmap.png
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PASTA_PROJETO = Path(__file__).resolve().parent.parent
ARQUIVO_CSV = PASTA_PROJETO / "dados" / "dados_heatmap.csv"
ARQUIVO_IMAGEM = PASTA_PROJETO / "imagens" / "heatmap.png"

try:
    df = pd.read_csv(ARQUIVO_CSV)
except FileNotFoundError:
    sys.exit(f"Arquivo não encontrado: {ARQUIVO_CSV}")

matriz = df.pivot(index="dia_semana", columns="horario", values="movimento_clientes")

ordem_dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
matriz = matriz.reindex(ordem_dias)

fig, ax = plt.subplots(figsize=(10, 6))

sns.heatmap(
    matriz,
    annot=True,        
    fmt="d",         
    cmap="YlOrRd",   
    linewidths=0.5,
    cbar_kws={"label": "Movimento de clientes"},
    ax=ax,
)

ax.set_title("Movimento de Clientes por Dia e Horário", fontsize=14, fontweight="bold")
ax.set_xlabel("Horário", fontsize=11)
ax.set_ylabel("Dia da semana", fontsize=11)
plt.yticks(rotation=0)

plt.tight_layout()
ARQUIVO_IMAGEM.parent.mkdir(exist_ok=True)
plt.savefig(ARQUIVO_IMAGEM, dpi=300, bbox_inches="tight")
print(f"Imagem salva em: {ARQUIVO_IMAGEM}")
plt.show()
