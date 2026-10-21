# Projeto de Visualização de Dados com Python

## Objetivo

Atividade escolar de programação: gerar **nove gráficos**, um para cada arquivo CSV fornecido, usando Python, Pandas, Matplotlib e Seaborn. Cada gráfico tem seu **próprio script independente**.

## Tecnologias

- Python 3
- Pandas (leitura e preparação dos dados)
- Matplotlib (construção e personalização dos gráficos)
- Seaborn (gráficos estatísticos)

## Estrutura de pastas

```text
projeto-graficos/
├── dados/              # arquivos CSV usados pelos scripts
│   ├── dados_dispersao.csv
│   ├── dados_distribuicao.csv
│   ├── dados_frequencia.csv
│   ├── dados_heatmap.csv
│   ├── dados_linhas.csv
│   ├── dados_pizza.csv
│   ├── dados_regressao.csv
│   ├── dados_barras.csv
│   └── dados_boxplot.csv
├── graficos/           # um script por gráfico
│   ├── dispersao.py
│   ├── distribuicao.py
│   ├── frequencia.py
│   ├── heatmap.py
│   ├── linhas.py
│   ├── pizza.py
│   ├── regressao.py
│   ├── barras.py
│   └── boxplot.py
├── imagens/            # imagens PNG geradas pelos scripts
├── requirements.txt
├── README.md
└── .gitignore
```

Os CSVs devem ficar na pasta `dados/`. As imagens geradas são salvas automaticamente na pasta `imagens/`.

## Os nove gráficos

| Script | CSV | Gráfico | O que mostra |
|---|---|---|---|
| `dispersao.py` | `dados_dispersao.csv` | Dispersão | Altura × peso, com cor por sexo |
| `distribuicao.py` | `dados_distribuicao.csv` | Distribuição | Histograma + curva de densidade da idade dos clientes |
| `frequencia.py` | `dados_frequencia.csv` | Frequência | Número de chamados por tipo de atendimento |
| `heatmap.py` | `dados_heatmap.csv` | Mapa de calor | Movimento de clientes por dia da semana e horário |
| `linhas.py` | `dados_linhas.csv` | Linhas | Evolução das vendas diárias (pontos coloridos por loja) |
| `pizza.py` | `dados_pizza.csv` | Pizza | Participação de cada canal de venda no faturamento |
| `regressao.py` | `dados_regressao.csv` | Regressão | Renda mensal × gasto mensal com linha de regressão |
| `barras.py` | `dados_barras.csv` | Barras | Vendas médias por categoria e região |
| `boxplot.py` | `dados_boxplot.csv` | Boxplot | Distribuição de salários por departamento (outliers mantidos) |

## Instalação (Windows, terminal do VS Code)

Abra o terminal **na pasta raiz do projeto** (a pasta que contém `requirements.txt`) e execute:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows CMD:

```bat
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como executar

Cada script é independente e pode ser executado sozinho. Com o terminal na raiz do projeto:

```bash
python graficos/dispersao.py
python graficos/distribuicao.py
python graficos/frequencia.py
python graficos/heatmap.py
python graficos/linhas.py
python graficos/pizza.py
python graficos/regressao.py
python graficos/barras.py
python graficos/boxplot.py
```

Cada script abre o gráfico em uma janela (`plt.show()`) e também salva a imagem em `imagens/`. Os caminhos são calculados a partir da localização do próprio script, então o comando funciona mesmo a partir de outra pasta, desde que o caminho do script esteja correto.

## Publicação no GitHub

1. Crie um repositório vazio no GitHub (por exemplo, `projeto-graficos`).
2. Na raiz do projeto, execute:

```bash
git init
git add .
git commit -m "Projeto de visualização de dados"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/projeto-graficos.git
git push -u origin main
```

3. Envie ao professor o link do repositório.
