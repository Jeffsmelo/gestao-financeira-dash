from dash import Input, Output
from services.auth_service import is_master


def registrar_filtro_cc_callbacks(app):

    @app.callback(
        [
            Output("filtro-cc", "style"),
            Output("filtro-cc", "disabled"),
        ],
        Input("usuario-logado", "data"),
    )
    def controlar_filtro_cc(usuario):

        if not usuario:
            return {"display": "none"}, True

        if is_master(usuario):
            return {"display": "block"}, False

        return {"display": "none"}, True