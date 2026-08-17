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

    from services.auth_service import get_cc_permitidos, is_master

    cc_permitidos = get_cc_permitidos(usuario)

    # 🔒 Contas ocultas (somente Admin pode ver)
    contas_ocultas = [
        "4010101001", "4010101002", "4010101003", "4010101004",
        "4010101005", "4010101006", "4010101007", "4010101009",
        "4010101010", "4010101011", "4010101012", "4010101013",
        "4010101016", "4010101017", "4010101018", "4010101019",
        "4010101020", "4010101021", "4010101024", "4010101025",
        "4010101026", "4010101027", "4010101028", "4010101029",
        "4010101030", "4010101032", "4010101033", "4010101035",
        "4010101037", "4010101038",

        "4010202039",

        "4010204001", "4010204002", "4010204003", "4010204004",
        "4010204005", "4010204006", "4010204007", "4010204008",
        "4010204009", "4010204010", "4010204012", "4010204013",
        "4010204014", "4010204015", "4010204016", "4010204017",
        "4010204018", "4010204019", "4010204021", "4010204024",
        "4010204025", "4010204026", "4010204027", "4010204029",
        "4010204032", "4010204034", "4010204035",

        "4010205047"
    ]

    # 🔐 Usuário comum → força CC único
    if not is_master(usuario):
        if not cc_permitidos:
            return pd.DataFrame()
        cc = cc_permitidos[0]

    # ================================
    # ✅ QUERY PRINCIPAL
    # ================================
    query = """
        SELECT
            [CC],
            [Conta],
            [Descrição Conta],
            [Realizado],
            [Histórico] AS Historico,
            [Data],
            [Descricao],
            YEAR([Data]) AS Ano,
            RIGHT('0' + CAST(MONTH([Data]) AS VARCHAR), 2) AS Mes
        FROM VW_MN_ATUALIZACAO_DESPESAS
        WHERE 1=1
    """

    params = []

    # 🔥 Usuário comum NÃO vê contas ocultas
    if usuario != "Admin":
        placeholders = ",".join(["?"] * len(contas_ocultas))
        query += f" AND [Conta] NOT IN ({placeholders})"
        params.extend(contas_ocultas)

    # 🎯 Filtro CC
    if cc:
        query += " AND [CC] = ?"
        params.append(cc)

    # 🎯 Filtro Ano
    if ano:
        query += " AND YEAR([Data]) = ?"
        params.append(ano)

    # 🎯 Filtro Meses
    if meses:
        placeholders = ",".join(["?"] * len(meses))
        query += f"""
            AND RIGHT('0' + CAST(MONTH([Data]) AS VARCHAR), 2)
            IN ({placeholders})
        """
        params.extend(meses)

    query += " ORDER BY [Data] DESC"

    # ================================
    # ✅ EXECUTAR QUERY
    # ================================
    df = pd.read_sql(query, engine, params=tuple(params))

    if df.empty:
        return df

    # Ajustes finais
    df["Realizado"] = pd.to_numeric(df["Realizado"], errors="coerce").fillna(0)
    df["Data"] = pd.to_datetime(df["Data"])

    return df
