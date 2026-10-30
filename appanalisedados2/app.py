"""Dashboard Streamlit com os nove gráficos da atividade 06.

Como executar (na raiz do projeto):
    streamlit run app.py
"""
from pathlib import Path

import streamlit as st

NOME_ALUNO = "Seu Nome Completo"
NUMERO_CHAMADA = "00"
TURMA = "Sua Turma"

PASTA_IMAGENS = Path(__file__).resolve().parent / "imagens"

LINHAS = [
    [
        (
            "Dispersão — Altura × Peso",
            "dispersao.png",
            "Há uma relação positiva forte entre altura e peso (correlação de "
            "cerca de 0,85): quanto mais alta a pessoa, maior tende a ser o peso. "
            "As médias dos dois sexos são parecidas (≈ 170 cm; 62–63 kg), e os "
            "pontos de ambos se misturam ao longo da nuvem.",
        ),
        (
            "Distribuição — Idade dos clientes",
            "distribuicao.png",
            "A idade vai de 18 a 69 anos, com média de 33,6 e mediana de 29. "
            "A curva tem dois picos: um grupo jovem, em torno de 25 anos, e outro "
            "menor perto dos 47. Poucos clientes passam dos 60 anos.",
        ),
        (
            "Frequência — Tipos de atendimento",
            "frequencia.png",
            "Dos 300 chamados, 116 (38,7%) são dúvidas, seguidas por reclamações "
            "(73; 24,3%) e bugs (49; 16,3%). Cancelamentos (33) e elogios (29) "
            "são os menos frequentes. As reclamações superam os elogios "
            "em mais de 2,5 vezes.",
        ),
    ],
    [
        (
            "Mapa de calor — Movimento de clientes",
            "heatmap.png",
            "O fim de semana concentra o maior movimento: o pico é domingo às "
            "12h (199 clientes) e a média de domingo (≈ 119) e sábado (≈ 111) "
            "é bem superior à dos dias úteis. O menor valor é quinta às 16h (22), "
            "e quinta é o dia útil mais fraco (média ≈ 44).",
        ),
        (
            "Linhas — Vendas diárias",
            "linhas.png",
            "As vendas crescem ao longo do trimestre: a média mensal sobe de "
            "≈ 122 em janeiro para ≈ 173 em fevereiro e ≈ 225 em março. "
            "Há oscilações de um dia para o outro, mas a tendência é de alta. "
            "O menor valor foi 93,21 e o maior, 260,37. As duas lojas "
            "aparecem em quantidade parecida de registros.",
        ),
        (
            "Pizza — Faturamento por canal",
            "pizza.png",
            "De um faturamento total de 120.000, o Site responde por 37,5% e a "
            "Loja Física por 26,7%: juntos somam mais de 64%. O Aplicativo tem "
            "17,5%, Parceiros 11,7% e o Telefone, apenas 6,7%.",
        ),
    ],
    [
        (
            "Regressão — Renda × Gasto",
            "regressao.png",
            "A relação é positiva e muito forte (correlação ≈ 0,99): os pontos "
            "ficam bem perto da reta. Em média, cada R$ 1.000 a mais de renda "
            "vem acompanhado de cerca de R$ 570 a mais de gasto. "
            "Isso mostra associação entre as variáveis, não causa e efeito.",
        ),
        (
            "Barras — Vendas médias por categoria e região",
            "barras.png",
            "O maior valor é Livros na região Oeste (284,18) e o menor, "
            "Alimentos no Norte (54,15). A região Oeste tem a maior média "
            "(≈ 225) e o Norte, a menor (≈ 103). Entre as categorias, "
            "Livros lidera (média ≈ 187).",
        ),
        (
            "Boxplot — Salários por departamento",
            "boxplot.png",
            "Vendas (mediana ≈ 7.130) e TI (≈ 6.614) pagam mais que Marketing "
            "(≈ 4.191) e RH (≈ 4.188). Cada departamento tem 2 salários atípicos "
            "bem acima dos demais (até 21.000 em TI e Vendas; 12.000 em Marketing "
            "e RH), que foram mantidos no gráfico.",
        ),
    ],
]


def mostrar_grafico(titulo, arquivo, analise):
    """Mostra um gráfico e, logo abaixo, a análise dele."""
    st.markdown(f"##### {titulo}")
    caminho = PASTA_IMAGENS / arquivo
    if caminho.exists():
        st.image(str(caminho), width="stretch")
    else:
        st.error(f"Imagem não encontrada: {arquivo}. Execute o script correspondente.")
    st.markdown(f"**Análise:** {analise}")

st.set_page_config(
    page_title="Dashboard de Gráficos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.header("Informações do aluno")
    st.write(f"**Nome:** {NOME_ALUNO}")
    st.write(f"**Nº da chamada:** {NUMERO_CHAMADA}")
    st.write(f"**Turma:** {TURMA}")

st.title("📊 Dashboard de Visualização de Dados")
st.caption("Atividade de Fixação 07 — gráficos gerados na atividade 06")

for numero, linha in enumerate(LINHAS):
    if numero > 0:
        st.divider()
    colunas = st.columns(3)
    for coluna, (titulo, arquivo, analise) in zip(colunas, linha):
        with coluna:
            mostrar_grafico(titulo, arquivo, analise)
