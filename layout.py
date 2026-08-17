import dash_bootstrap_components as dbc
from dash import html, dcc

def layout_principal(usuario):

    return html.Div(
        [

            # ========================
            # FILTROS
            # ========================
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Dropdown(
                            id="filtro-ano",
                            placeholder="Selecione o ano",
                        ),
                        md=3,
                    ),

                    dbc.Col(
                        dcc.Dropdown(
                            id="filtro-mes",
                            multi=True,
                            placeholder="Selecione o(s) mês(es)",
                        ),
                        md=4,
                    ),

                    # 🔴 FILTRO CC — EXISTE SEMPRE
                    dbc.Col(
                        dcc.Dropdown(
                            id="filtro-cc",
                            placeholder="Centro de Custo",
                            disabled=True,
                            style={"display": "none"},
                        ),
                        md=3,
                    ),
                ],
                className="mb-3",
            ),

            html.Div(id="kpi-cards"),
            html.Div(id="tabela-despesas"),
        ]
    )