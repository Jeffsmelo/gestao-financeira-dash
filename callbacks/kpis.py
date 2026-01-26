from dash import html, Input, Output
from services.despesas_service import get_despesas


def registrar_kpis_callbacks(app):

    @app.callback(
        Output("kpi-cards", "children"),
        [
            Input("filtro-ano", "value"),
            Input("filtro-mes", "value"),
            Input("filtro-cc", "value"),
            Input("usuario-logado", "data"),
        ]
    )
    def atualizar_kpis(ano, meses, cc, usuario):

        if not usuario or not ano:
            return html.Div("Selecione os filtros para visualizar os indicadores.")

        df = get_despesas(
            usuario=usuario,
            ano=ano,
            meses=meses,
            cc=cc
        )

        if df.empty:
            return html.Div("Nenhum dado encontrado para os filtros selecionados.")

        total = df["Realizado"].sum()
        quantidade = len(df)

        meses_usados = df["Mes"].nunique() if "Mes" in df.columns else 1
        media_mensal = total / meses_usados if meses_usados else total

        def card(titulo, valor):
            return html.Div(
                [
                    html.H4(titulo),
                    html.H2(valor)
                ],
                style={
                    "backgroundColor": "#FFFFFF",
                    "padding": "20px",
                    "borderRadius": "10px",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
                    "width": "240px",
                    "textAlign": "center"
                }
            )

        return [
            card(
                "💰 Total Realizado",
                f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            ),
            card("📄 Lançamentos", quantidade),
            card(
                "📊 Média Mensal",
                f"R$ {media_mensal:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            )
        ]