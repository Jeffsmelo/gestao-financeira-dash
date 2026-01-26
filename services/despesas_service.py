import pandas as pd
from config.database import engine


def listar_anos_disponiveis():
    query = """
        SELECT DISTINCT
            YEAR([Data]) AS Ano
        FROM VW_MN_ATUALIZACAO_DESPESAS
        ORDER BY Ano DESC
    """
    return pd.read_sql(query, engine)


def listar_cc_disponiveis():
    query = """
        SELECT DISTINCT
            CC
        FROM VW_MN_ATUALIZACAO_DESPESAS
        ORDER BY CC
    """
    return pd.read_sql(query, engine)


def get_despesas(usuario, ano, meses=None, cc=None):
    """
    Retorna despesas filtradas por:
    - usuário (controle de CC)
    - ano
    - meses (lista '01','02',...)
    - centro de custo (somente admin)
    """

    from services.auth_service import get_cc_permitidos, is_master

    cc_permitidos = get_cc_permitidos(usuario)

    # 🔐 Usuário comum → força CC único
    if not is_master(usuario):
        if not cc_permitidos:
            return pd.DataFrame()
        cc = cc_permitidos[0]

    query = """
        SELECT
            [CC],
            [Conta],
            [Descrição Conta],
            [Realizado],
            [Histórico] AS Historico,
            [Data],
            YEAR([Data]) AS Ano,
            RIGHT('0' + CAST(MONTH([Data]) AS VARCHAR), 2) AS Mes
        FROM VW_MN_ATUALIZACAO_DESPESAS
        WHERE 1=1
    """

    params = []

    if cc:
        query += " AND [CC] = ?"
        params.append(cc)

    if ano:
        query += " AND YEAR([Data]) = ?"
        params.append(ano)

    if meses:
        placeholders = ",".join(["?"] * len(meses))
        query += f"""
            AND RIGHT('0' + CAST(MONTH([Data]) AS VARCHAR), 2)
            IN ({placeholders})
        """
        params.extend(meses)

    query += " ORDER BY [Data] DESC"

    df = pd.read_sql(query, engine, params=tuple(params))

    if df.empty:
        return df

    df["Realizado"] = pd.to_numeric(df["Realizado"], errors="coerce").fillna(0)
    df["Data"] = pd.to_datetime(df["Data"])

    return df