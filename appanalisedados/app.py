from pathlib import Path
import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUT_DIR = BASE_DIR / "output"

TZ = "America/Sao_Paulo"
LIMITE_VALOR = 5_000.0
LIMITE_Z = 2.5

RISCO_DICT = {
    "C100": "Baixo",
    "C101": "Alto",
    "C102": "Médio",
    "C103": "Baixo",
    "C104": "Alto",
}
def gerar_dados() -> None:
    """Gera os arquivos brutos transacoes.csv (latin1) e cotacoes.csv (utf-8)."""
    DATA_DIR.mkdir(exist_ok=True)
    np.random.seed(42)

    # --- transacoes.csv ---
    datas = pd.date_range(start="2026-09-01", periods=1000, freq="h")
    df = pd.DataFrame({
        "id_cliente": np.random.choice(["C100", "C101", "C102", "C103", "C104"], size=1000),
        "data_transacao": datas,
        "valor": np.random.choice(
            [np.nan, 150.0, 3000.0, 7500.0, 12000.0, 50.0],
            size=1000,
            p=[0.05, 0.40, 0.30, 0.15, 0.05, 0.05],
        ),
        "estado_cliente": np.random.choice(["SP", "RJ", "MG", "RS"], size=1000),
        "origem": np.random.choice(["web", "mobile_app", "atm"], size=1000),
    })
    df = pd.concat([df, df.iloc[:15]], ignore_index=True)  
    df.to_csv(DATA_DIR / "transacoes.csv", index=False, encoding="latin1")

    datas_c = pd.date_range(start="2026-09-01", end="2026-10-01", freq="D")
    variacoes = np.random.normal(loc=0.001, scale=0.015, size=len(datas_c))
    precos = 5.20 * np.exp(np.cumsum(variacoes))
    cot = pd.DataFrame({
        "data": datas_c,
        "cotacao_usd": np.round(precos, 4),
        "volume_negociado": np.random.randint(10000, 500000, size=len(datas_c)),
    })
    cot.loc[5, "cotacao_usd"] = np.nan
    cot.loc[18, "cotacao_usd"] = np.nan
    cot.to_csv(DATA_DIR / "cotacoes.csv", index=False, encoding="utf-8")

    print("Arquivos 'transacoes.csv' e 'cotacoes.csv' gerados com sucesso!")

def carregar_transacoes(caminho: Path) -> pd.DataFrame:
    """Lê o CSV em latin1 (encoding legado) e cria a coluna `plataforma`."""
    df = pd.read_csv(
        caminho,
        encoding="latin1",
        dtype={"id_cliente": "string", "origem": "category", "estado_cliente": "category"},
        parse_dates=["data_transacao"],
    )
    df["plataforma"] = "Mobile"  
    return df


def imputar_valor_mediana_estado(df: pd.DataFrame) -> pd.DataFrame:
    """Substitui NaN de `valor` pela mediana do respectivo estado."""
    mediana_estado = df.groupby("estado_cliente", observed=True)["valor"].transform("median")
    df["valor"] = df["valor"].fillna(mediana_estado)
    return df

def tratar_datas(df: pd.DataFrame) -> pd.DataFrame:
    df["data_transacao"] = pd.to_datetime(df["data_transacao"]).astype("datetime64[ns]")
    df["data_transacao"] = df["data_transacao"].dt.tz_localize(TZ)
    df["dia_semana"] = df["data_transacao"].dt.day_name()
    df["mes"] = df["data_transacao"].dt.month
    return df

def filtrar_setembro_alto_valor(df: pd.DataFrame) -> pd.DataFrame:
    mask = (
        (df["mes"] == 9)
        & ((df["estado_cliente"] == "SP") | (df["estado_cliente"] == "RJ"))
        & (df["valor"] > LIMITE_VALOR)
    )
    return df[mask]

def adicionar_risco(df: pd.DataFrame, risco_dict: dict) -> pd.DataFrame:
    df["nivel_risco"] = df["id_cliente"].astype(str).map(risco_dict)
    return df


def tabela_dinamica(df: pd.DataFrame) -> pd.DataFrame:
    return pd.pivot_table(
        df,
        values="valor",
        index="mes",
        columns="nivel_risco",
        aggfunc="sum",
        margins=True,
        margins_name="Total",
    )


def calcular_zscore(df: pd.DataFrame, coluna: str = "valor", grupo: str = "estado_cliente") -> pd.Series:
    """Z = (x - mu) / sigma por grupo, totalmente vetorizado (sem laços for)."""
    g = df.groupby(grupo, observed=True)[coluna]
    mu = g.transform("mean")
    sigma = g.transform("std")
    return (df[coluna] - mu) / sigma.replace(0, np.nan)


def detectar_anomalias(df: pd.DataFrame) -> pd.DataFrame:
    df = df.assign(zscore=calcular_zscore(df))
    return df[df["zscore"] > LIMITE_Z].copy()

def gerar_grafico(df: pd.DataFrame, destino: Path) -> None:
    diario = df.set_index("data_transacao")["valor"].resample("D").sum()
    media_movel = diario.rolling(7).mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(diario.index, diario.values, label="Valor total diário", color="#1f77b4", linewidth=1.5)
    ax.plot(media_movel.index, media_movel.values, label="Média móvel (7 dias)",
            color="#d62728", linewidth=2.5)

    ax.set_ylim(bottom=0)
    ax.set_title("Volume Financeiro Diário de Transações e Média Móvel de 7 Dias", fontsize=14)
    ax.set_xlabel("Data")
    ax.set_ylabel("Valor total (R$)")
    ax.yaxis.set_major_formatter(lambda x, _: f"R$ {x:,.0f}".replace(",", "."))
    ax.grid(alpha=0.3)
    ax.legend(loc="upper right")
    fig.autofmt_xdate()
    fig.tight_layout()

    destino.parent.mkdir(exist_ok=True)
    fig.savefig(destino, dpi=150)
    plt.close(fig)


def consolidar_cotacoes(df: pd.DataFrame, caminho: Path) -> pd.DataFrame:
    cot = pd.read_csv(caminho, encoding="utf-8", parse_dates=["data"])
    cot["cotacao_usd"] = cot["cotacao_usd"].interpolate(limit_direction="both")
    df = df.assign(data=df["data_transacao"].dt.tz_localize(None).dt.normalize())
    df = df.merge(cot, on="data", how="left")
    df["valor_usd"] = df["valor"] / df["cotacao_usd"]
    return df.drop(columns="data")

def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)

    if not (DATA_DIR / "transacoes.csv").exists() or not (DATA_DIR / "cotacoes.csv").exists():
        gerar_dados()

    df = carregar_transacoes(DATA_DIR / "transacoes.csv")
    print(f"Linhas brutas: {len(df)} | NaN em valor: {df['valor'].isna().sum()}")

    df = tratar_datas(df)

    # Duplicatas removidas antes da imputação para não enviesar as medianas.
    antes = len(df)
    df = df.drop_duplicates(keep="first").reset_index(drop=True)
    print(f"Duplicatas removidas: {antes - len(df)}")

    df = imputar_valor_mediana_estado(df)
    df = adicionar_risco(df, RISCO_DICT)
    df = consolidar_cotacoes(df, DATA_DIR / "cotacoes.csv")

    filtradas = filtrar_setembro_alto_valor(df)
    print(f"\nSetembro, SP/RJ e valor > R$ 5.000: {len(filtradas)} transações")

    pivot = tabela_dinamica(df)
    print("\nTabela dinâmica (soma de valor por mês x risco):")
    print(pivot.round(2).to_string())

    anomalias = detectar_anomalias(df)
    print(f"\nAnomalias (Z > {LIMITE_Z}): {len(anomalias)}")

    gerar_grafico(df, OUT_DIR / "grafico_transacoes_diarias.png")

    df.to_csv(OUT_DIR / "transacoes_limpas.csv", index=False)
    filtradas.to_csv(OUT_DIR / "filtro_setembro_sp_rj.csv", index=False)
    pivot.to_csv(OUT_DIR / "pivot_mes_risco.csv")
    anomalias.to_csv(OUT_DIR / "anomalias_zscore.csv", index=False)
    print(f"\nArquivos salvos em: {OUT_DIR}")


if __name__ == "__main__":
    main()