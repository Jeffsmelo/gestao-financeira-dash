from dash import Input, Output, State, html, no_update
from dash.exceptions import PreventUpdate
from services.auth_service import USUARIOS_CC, is_master

def registrar_login_callbacks(app):

    @app.callback(
        Output("login-msg", "children"),
        Output("usuario-logado", "data"),
        Input("btn-login", "n_clicks"),
        State("login-usuario", "value"),
        State("login-senha", "value"),
        prevent_initial_call=True
    )
    def processar_login(n_clicks, usuario, senha):

        if not n_clicks:
            raise PreventUpdate

        # 🔹 Campos vazios → aviso leve
        if not usuario or not senha:
            return (
                html.Span("⚠️ Preencha usuário e senha.", style={"color": "orange"}),
                no_update
            )

        # 🔐 Validação real
        if usuario in USUARIOS_CC and senha in USUARIOS_CC[usuario]:
            # ✅ LOGIN OK → NÃO MOSTRA MENSAGEM
            return "", usuario

        # ❌ LOGIN INVÁLIDO → MOSTRA ERRO
        return (
            html.Span("❌ Usuário ou senha inválidos.", style={"color": "red"}),
            no_update
        )

    @app.callback(
        Output("login-senha", "type"),
        Input("btn-toggle-senha", "n_clicks"),
        State("login-senha", "type"),
        prevent_initial_call=True
    )
    def alternar_visibilidade_senha(n_clicks, tipo_atual):
        if tipo_atual == "password":
            return "text"
        return "password"
