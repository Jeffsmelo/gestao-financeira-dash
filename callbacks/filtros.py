from dash import Input, Output
import pandas as pd

from config.database import engine
from services.auth_service import is_master
from services.despesas_service import listar_anos_disponiveis, listar_cc_disponiveis


def registrar_filtros_callbacks(app):

    # =====================================================
    # 🔹 ANOS DISPONÍVEIS
    # =====================================================
    @app.callback(
        Output("filtro-ano", "options"),
        Input("usuario-logado", "data")
    )
    def carregar_anos(usuario):

        if not usuario:
            return []

        df = listar_anos_disponiveis()
        return [{"label": str(ano), "value": ano} for ano in df["Ano"]]


    # =====================================================
    # 🔹 MESES (options)
    # =====================================================
    @app.callback(
    Output("filtro-mes", "options"),
    Input("filtro-ano", "value")
    )
    def carregar_meses(ano):

        if not ano:
            return []

        query = """
            SELECT DISTINCT
                RIGHT('0' + CAST(MONTH([Data]) AS VARCHAR), 2) AS Mes
            FROM VW_MN_ATUALIZACAO_DESPESAS
            WHERE YEAR([Data]) = ?
            ORDER BY Mes
        """

        df = pd.read_sql(
            query,
            engine,
            params=(ano,)   # ✅ TUPLA, não lista
        )

        nomes_meses = {
            "01": "Janeiro",
            "02": "Fevereiro",
            "03": "Março",
            "04": "Abril",
            "05": "Maio",
            "06": "Junho",
            "07": "Julho",
            "08": "Agosto",
            "09": "Setembro",
            "10": "Outubro",
            "11": "Novembro",
            "12": "Dezembro",
        }

        return [
            {"label": nomes_meses.get(mes, mes), "value": mes}
            for mes in df["Mes"]
        ]



    # =====================================================
    # 🔹 RESET MESES AO TROCAR ANO  🔥
    # =====================================================
    @app.callback(
        Output("filtro-mes", "value"),
        Input("filtro-ano", "value")
    )
    def resetar_meses(_):
        return []


    # =====================================================
    # 🔹 CENTRO DE CUSTO (APENAS ADMIN)
    # =====================================================
    @app.callback(
        Output("filtro-cc", "options"),
        Input("usuario-logado", "data")
    )
    def carregar_cc(usuario):

        if not usuario or not is_master(usuario):
            return []

        df = listar_cc_disponiveis()
        return [{"label": cc, "value": cc} for cc in df["CC"]]


    # =====================================================
    # 🔹 RESET CC AO TROCAR USUÁRIO
    # =====================================================
    @app.callback(
        Output("filtro-cc", "value"),
        Input("usuario-logado", "data")
    )
    def resetar_cc(_):
        return None