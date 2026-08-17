from dash import Dash, html, dcc, Input, Output
from layouts.login import layout_login
from layouts.main_layout import layout_principal

from callbacks.login import registrar_login_callbacks
from callbacks.filtros import registrar_filtros_callbacks
from callbacks.kpis import registrar_kpis_callbacks
from callbacks.tabela import registrar_tabela_callbacks
from callbacks.filtro_cc import registrar_filtro_cc_callbacks

app = Dash(__name__, suppress_callback_exceptions=True)

# ✅ LAYOUT RAIZ (TODOS OS IDS EXISTEM AQUI)
app.layout = html.Div([

    # Estado global
    dcc.Store(id="usuario-logado"),

    # 🔴 FILTRO CC "FANTASMA" (necessário para o Dash)
    dcc.Dropdown(
        id="filtro-cc",
        style={"display": "none"},
        disabled=True
    ),

    # Conteúdo dinâmico
    html.Div(id="conteudo-principal")
])

# 🔌 Registrar callbacks
registrar_login_callbacks(app)
registrar_filtros_callbacks(app)
registrar_kpis_callbacks(app)
registrar_tabela_callbacks(app)
registrar_filtro_cc_callbacks(app)


@app.callback(
    Output("conteudo-principal", "children"),
    Input("usuario-logado", "data")
)
def renderizar(usuario):
    if not usuario:
        return layout_login()
    return layout_principal(usuario)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=9765,
        debug=False
    )