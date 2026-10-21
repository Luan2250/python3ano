"""Gráfico de frequência: quantidade de chamados por tipo de atendimento.

Dados: dados/dados_frequencia.csv (id_chamado, tipo_atendimento)
Saída: imagens/frequencia.png
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PASTA_PROJETO = Path(__file__).resolve().parent.parent
ARQUIVO_CSV = PASTA_PROJETO / "dados" / "dados_frequencia.csv"
ARQUIVO_IMAGEM = PASTA_PROJETO / "imagens" / "frequencia.png"

try:
    df = pd.read_csv(ARQUIVO_CSV)
except FileNotFoundError:
    sys.exit(f"Arquivo não encontrado: {ARQUIVO_CSV}")

ordem = df["tipo_atendimento"].value_counts().index

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(9, 6))

sns.countplot(
    data=df,
    x="tipo_atendimento",
    order=ordem,
    color="#4c72b0",
    ax=ax,
)

ax.bar_label(ax.containers[0], padding=3)

ax.set_title("Frequência por Tipo de Atendimento", fontsize=14, fontweight="bold")
ax.set_xlabel("Tipo de atendimento", fontsize=11)
ax.set_ylabel("Número de chamados", fontsize=11)

plt.tight_layout()
ARQUIVO_IMAGEM.parent.mkdir(exist_ok=True)
plt.savefig(ARQUIVO_IMAGEM, dpi=300, bbox_inches="tight")
print(f"Imagem salva em: {ARQUIVO_IMAGEM}")
plt.show()
