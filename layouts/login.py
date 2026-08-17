from dash import html, dcc

def layout_login():
    return html.Div(
        [
            html.Div(
                [
                    # 🔐 Título
                    html.H4(
                        "🔐 Login",
                        style={
                            "textAlign": "center",
                            "marginBottom": "20px"
                        }
                    ),

                    # 👤 Usuário
                    html.Label("👤 Usuário"),
                    dcc.Input(
                        id="login-usuario",
                        type="text",
                        placeholder="Digite seu centro de custo",
                        style={
                            "width": "100%",
                            "height": "38px",
                            "padding": "6px 40px 6px 10px",
                            "boxSizing": "border-box"
                        }
                    ),

                    # 🔑 Senha + botão 👁️
                    html.Label("🔑 Senha"),

                    html.Div(
                        [
                            dcc.Input(
                                id="login-senha",
                                type="password",
                                placeholder="Digite sua senha",
                                style={
                                    "width": "100%",
                                    "height": "38px",
                                    "padding": "6px 40px 6px 10px",
                                    "boxSizing": "border-box"
                                }
                            ),

                            html.Button(
                                "👁️",
                                id="btn-toggle-senha",
                                n_clicks=0,
                                style={
                                    "position": "absolute",
                                    "right": "10px",
                                    "top": "50%",
                                    "transform": "translateY(-50%)",
                                    "border": "none",
                                    "background": "transparent",
                                    "cursor": "pointer",
                                    "fontSize": "18px",
                                    "padding": "0",
                                    "lineHeight": "1"
                                }
                            ),
                        ],
                        style={
                            "position": "relative",
                            "marginBottom": "20px"
                        }
                    ),

                    # ⏳ Botão Entrar com spinner
                    dcc.Loading(
                        id="loading-login",
                        type="circle",
                        children=[
                            html.Button(
                                "Entrar",
                                id="btn-login",
                                n_clicks=0,
                                style={
                                    "width": "100%",
                                    "padding": "10px",
                                    "backgroundColor": "#ff0202",
                                    "color": "white",
                                    "border": "none",
                                    "borderRadius": "6px",
                                    "cursor": "pointer",
                                    "fontWeight": "500"
                                }
                            )
                        ]
                    ),

                    # ❌ Mensagem de erro / aviso
                    html.Div(
                        id="login-msg",
                        style={
                            "marginTop": "15px",
                            "textAlign": "center",
                            "fontWeight": "500"
                        }
                    ),
                ],
                style={
                    "width": "350px",
                    "padding": "25px",
                    "borderRadius": "10px",
                    "boxShadow": "0px 4px 12px rgba(0,0,0,0.1)",
                    "backgroundColor": "white"
                }
            )
        ],
        style={
            "height": "100vh",
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center",
            "backgroundColor": "#f8f9fa"
        }
    )