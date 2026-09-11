import pandas as pd  # type: ignore
import sqlite3

pd.set_option("display.width", 140)
pd.set_option("display.max_columns", None)

print("=== ETAPA 1: EXTRAÇÃO DE DADOS ===")

vendas_loja = pd.read_csv("vendas_loja.csv")
vendas_loja["origem"] = "Física"
vendas_loja["data_venda"] = "2026-09-01"

vendas_site = pd.read_excel("vendas_site.xlsx")
vendas_site["origem"] = "Online"
vendas_site["data_venda"] = "2026-09-02"

clientes = pd.read_json("clientes.json")

imposto_regiao = pd.read_json("aliquota.json", typ="series")
imposto_regiao.name = "aliquota_imposto"

with sqlite3.connect("catalogo.db") as conn:
    produtos = pd.read_sql("SELECT * FROM produtos", con=conn)

print("Dados extraídos com sucesso!")

print("\n=== ETAPA 3: TRATAMENTO E INTEGRAÇÃO DE DATAFRAMES ===")

vendas_consolidadas = pd.concat([vendas_loja, vendas_site], ignore_index=True)
series_datas = pd.to_datetime(vendas_consolidadas["data_venda"])
series_dias_semana = series_datas.dt.day_name()

print("\nSeries derivada (Dias da semana):")
print(series_dias_semana)
vendas_consolidadas["desconto"] = vendas_consolidadas["desconto"].fillna(0.0)
vendas_consolidadas = vendas_consolidadas.drop_duplicates()

df_completo = vendas_consolidadas.merge(
    produtos, on="produto_id", how="left", indicator="_merge_produto"
)
df_completo = df_completo.merge(
    clientes, on="cliente_id", how="left", indicator="_merge_cliente"
)

sem_produto = df_completo[df_completo["_merge_produto"] == "left_only"]
sem_cliente = df_completo[df_completo["_merge_cliente"] == "left_only"]

print(f"\n--- AUDITORIA DE INTEGRAÇÕES ---")
print(f"Transações com produto_id não cadastrado: {len(sem_produto)}")
if not sem_produto.empty:
    print(sem_produto[["transacao_id", "produto_id", "origem"]])

print(f"Transações com cliente_id não cadastrado: {len(sem_cliente)}")
if not sem_cliente.empty:
    print(sem_cliente[["transacao_id", "cliente_id", "origem"]])

df_completo = df_completo[
    (df_completo["_merge_produto"] == "both") & (df_completo["_merge_cliente"] == "both")
].drop(columns=["_merge_produto", "_merge_cliente"])

df_completo["imposto"] = df_completo["estado"].map(imposto_regiao)

print("\nDataFrame Integrado e Tratado (pós-auditoria):")
print(df_completo[["transacao_id", "nome", "nome_produto", "origem", "desconto", "imposto"]])

print("\n=== ETAPA 3B: SANITIZAÇÃO E REGRAS DE NEGÓCIO ===")

n_antes = len(df_completo)

registros_invalidos = df_completo[
    (df_completo["quantidade"] <= 0)
    | (df_completo["preco_unitario"] <= 0)
    | (df_completo["desconto"] > 1.0)
]
if not registros_invalidos.empty:
    print("Registros inconsistentes removidos:")
    print(registros_invalidos[["transacao_id", "quantidade", "preco_unitario", "desconto"]])

df_completo = df_completo[
    (df_completo["quantidade"] > 0)
    & (df_completo["preco_unitario"] > 0)
    & (df_completo["desconto"] <= 1.0)
].copy()

print(f"\nRegistros antes da sanitização: {n_antes} | depois: {len(df_completo)}")

print("\n=== ETAPA 4: AGREGAÇÃO E MÉTRICAS ===")
df_completo["faturamento_bruto"] = df_completo["quantidade"] * df_completo["preco_unitario"]
df_completo["faturamento_liquido"] = (
    df_completo["quantidade"]
    * df_completo["preco_unitario"]
    * (1 - df_completo["desconto"])
    * (1 - df_completo["imposto"])
)
df_completo["valor_desconto"] = df_completo["faturamento_bruto"] * df_completo["desconto"]
# Valor de imposto retido sobre o valor já líquido de desconto
df_completo["valor_imposto"] = (
    df_completo["faturamento_bruto"] * (1 - df_completo["desconto"]) * df_completo["imposto"]
)

print("\nFaturamento bruto x líquido x descontos/impostos concedidos (amostra):")
print(
    df_completo[
        [
            "transacao_id",
            "faturamento_bruto",
            "valor_desconto",
            "valor_imposto",
            "faturamento_liquido",
        ]
    ]
)

relatorio_final = pd.pivot_table(
    df_completo,
    values="faturamento_liquido",
    index="categoria",
    columns="origem",
    aggfunc="sum",
    fill_value=0.0,
    margins=True,
    margins_name="Total Geral",
)

relatorio_formatado = relatorio_final.map(lambda x: f"R$ {x:,.2f}")

print("\n--- RELATÓRIO FINAL: FATURAMENTO LÍQUIDO (R$) ---")
print(relatorio_formatado)

print("\n=== ETAPA 5: ANÁLISE DE CLIENTES E TICKET MÉDIO ===")

analise_clientes = df_completo.groupby("cliente_id").agg(
    nome=("nome", "first"),
    estado=("estado", "first"),
    n_compras=("transacao_id", "count"),
    faturamento_total=("faturamento_liquido", "sum"),
)
analise_clientes["ticket_medio"] = (
    analise_clientes["faturamento_total"] / analise_clientes["n_compras"]
)

top_clientes = analise_clientes.nlargest(5, "faturamento_total")

print("\nTicket médio por cliente:")
print(analise_clientes.sort_values("faturamento_total", ascending=False))

print("\nTop 5 clientes por faturamento (maior valor):")
print(top_clientes)

print("\n=== ETAPA 6: DESCONTO MÉDIO POR CATEGORIA ===")

desconto_medio_categoria = (
    df_completo.groupby("categoria")["desconto"].mean().sort_values(ascending=False)
)
desconto_medio_categoria = (desconto_medio_categoria * 100).round(2).astype(str) + "%"

print("\nDesconto médio concedido por categoria:")
print(desconto_medio_categoria)