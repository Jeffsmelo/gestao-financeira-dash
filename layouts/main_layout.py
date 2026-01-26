# layouts/main_layout.py

from dash import html, dcc
from services.auth_service import is_master


def layout_principal(usuario):
    """
    Layout principal após login
    """

    # 🔹 Filtros básicos
    filtros = html.Div(
        [
            html.Div(
                [
                    html.Label("Ano"),
                    dcc.Dropdown(
                        id="filtro-ano",
                        placeholder="Selecione o ano",
                        clearable=False
                    ),
                ],
                style={"width": "150px"}
            ),

            html.Div(
                [
                    html.Label("Mês"),
                    dcc.Dropdown(
                        id="filtro-mes",
                        multi=True,
                        placeholder="Selecione o(s) mês(es)"
                    ),
                ],
                style={"width": "250px"}
            ),
        ],
        style={
            "display": "flex",
            "gap": "30px",
            "alignItems": "flex-end",
        }
    )

    # 🔐 Filtro CC somente para Admin
    filtro_cc = html.Div()

    if is_master(usuario):
        filtro_cc = html.Div(
            [
                html.Label("Centro de Custo"),
                dcc.Dropdown(
                    id="filtro-cc",
                    placeholder="Selecione o CC"
                ),
            ],
            style={"width": "300px"}
        )

    # ⬇️ Botão Exportar (para TODOS os usuários)
    botao_exportar = html.Div(
        [
            html.Button(
                "⬇️ Exportar para Excel",
                id="btn-exportar-excel",
                n_clicks=0,
                style={
                    "backgroundColor": "#198754",
                    "color": "white",
                    "border": "none",
                    "padding": "10px 18px",
                    "borderRadius": "8px",
                    "cursor": "pointer",
                    "fontWeight": "500",
                }
            ),
            dcc.Download(id="download-excel-despesas"),
        ],
        style={
            "display": "flex",
            "justifyContent": "center",
            "marginBottom": "20px",
        }
    )

    return html.Div(
        [
            html.Div(
                [
                    # 📊 Título
                    html.H2(
                        "📊 Gestão Financeira - Despesas",
                        style={
                            "textAlign": "center",
                            "fontWeight": "600",
                            "letterSpacing": "0.5px",
                            "marginBottom": "10px"
                        }
                    ),

                    # 🔎 Filtros
                    html.Div(
                        [
                            filtros,
                            filtro_cc
                        ],
                        style={
                            "display": "flex",
                            "gap": "40px",
                            "justifyContent": "center",
                            "flexWrap": "wrap",
                            "marginBottom": "15px",
                        }
                    ),

                    # ⬇️ Exportação
                    botao_exportar,

                    html.Hr(),

                    # 📈 KPIs
                    html.Div(
                        id="kpi-cards",
                        style={
                            "display": "flex",
                            "gap": "20px",
                            "justifyContent": "center",
                            "flexWrap": "wrap",
                            "marginBottom": "20px",
                        }
                    ),

                    html.Hr(),

                    # 📋 Tabela
                    html.Div(
                        [
                            html.H4(
                                "Detalhamento de Despesas",
                                style={"textAlign": "center"}
                            ),
                            html.Div(id="tabela-despesas")
                        ]
                    ),
                ],
                style={
                    "width": "100%",
                    "padding": "20px 10px",
                }
            )
        ]
    )