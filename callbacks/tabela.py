from dash import Input, Output, State, html, dash_table, ctx, dcc, no_update
import dash_bootstrap_components as dbc
import pandas as pd

from services.despesas_service import get_despesas


def registrar_tabela_callbacks(app):

    # ================================
    # 📋 ATUALIZAÇÃO DA TABELA
    # ================================
    @app.callback(
        Output("tabela-despesas", "children"),
        [
            Input("filtro-ano", "value"),
            Input("filtro-mes", "value"),
            Input("filtro-cc", "value"),
            Input("usuario-logado", "data"),
        ],
    )
    def atualizar_tabela(ano, meses, cc, usuario):

        if not usuario or not ano:
            return html.Div("Selecione os filtros para visualizar os dados.")

        if meses:
            meses = [str(m).zfill(2) for m in meses]

        # 🔥 REGRA DEFINITIVA PARA ADMIN
        if usuario == "Admin":
            cc = None

        df = get_despesas(
            usuario=usuario,
            ano=ano,
            meses=meses,
            cc=cc
        )

        if df.empty:
            return html.Div("Nenhum dado encontrado.")

        # 📅 Formatar Data
        if "Data" in df.columns:
            df["Data"] = (
                pd.to_datetime(df["Data"], errors="coerce")
                .dt.strftime("%d/%m/%Y")
            )

        # 🔍 Botão por linha
        df["Ação"] = "🔍 Ver Histórico"

        total = df["Realizado"].sum()

        tabela = dash_table.DataTable(
            id="datatable-despesas",
            columns=[
                {"name": "CC", "id": "CC"},
                {"name": "Conta", "id": "Conta"},
                {"name": "Descrição", "id": "Descrição Conta"},
                {
                    "name": "Realizado (R$)",
                    "id": "Realizado",
                    "type": "numeric",
                    "format": {"specifier": ",.2f"}
                },
                {"name": "Data", "id": "Data"},
                {
                    "name": "Ação",
                    "id": "Ação",
                    "presentation": "markdown"
                },
            ],
            data=df.to_dict("records"),
            page_size=15,
            style_table={"overflowX": "auto"},
            style_cell={
                "padding": "8px",
                "fontFamily": "Arial",
                "fontSize": "14px",
                "textAlign": "left"
            },
            style_header={
                "backgroundColor": "#f0f0f0",
                "fontWeight": "bold"
            },
            style_data_conditional=[
                {
                    "if": {"column_id": "Realizado"},
                    "textAlign": "right"
                }
            ],
        )

        modal = dbc.Modal(
            [
                dbc.ModalBody(id="modal-historico-body"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Fechar",
                        id="fechar-modal-historico",
                        color="secondary"
                    )
                ),
            ],
            id="modal-historico",
            is_open=False,
            size="lg",
            centered=True,
        )

        return html.Div(
            [
                html.H5(
                    f"💰 Total Geral: R$ {total:,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", "."),
                    style={"textAlign": "center", "marginBottom": "15px"}
                ),
                tabela,
                modal
            ]
        )

    # ================================
    # 📄 MODAL HISTÓRICO
    # ================================
    @app.callback(
        Output("modal-historico", "is_open"),
        Output("modal-historico-body", "children"),
        Input("datatable-despesas", "active_cell"),
        Input("fechar-modal-historico", "n_clicks"),
        State("datatable-despesas", "data"),
        State("modal-historico", "is_open"),
        prevent_initial_call=True
    )
    def abrir_modal(active_cell, fechar, rows, is_open):

        if ctx.triggered_id == "fechar-modal-historico":
            return False, html.Div()

        if active_cell and active_cell["column_id"] == "Ação":
            registro = rows[active_cell["row"]]
            historico = registro.get("Historico", "Sem histórico disponível")

            return True, html.Div(
                [
                    html.H4(
                        "📄 Histórico",
                        style={
                            "textAlign": "center",
                            "fontWeight": "600",
                            "marginBottom": "16px"
                        }
                    ),
                    html.Div(
                        historico,
                        style={
                            "textAlign": "center",
                            "whiteSpace": "pre-wrap",
                            "fontSize": "16px",
                            "padding": "16px",
                            "backgroundColor": "#f8f9fa",
                            "border": "1px solid #e0e0e0",
                            "borderRadius": "10px",
                            "maxHeight": "250px",
                            "overflowY": "auto",
                            "lineHeight": "1.6",
                        }
                    ),
                ],
                style={
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "justifyContent": "center",
                }
            )

        return is_open, html.Div()

    # ================================
    # ⬇️ EXPORTAÇÃO PARA EXCEL
    # ================================
    @app.callback(
        Output("download-excel-despesas", "data"),
        Input("btn-exportar-excel", "n_clicks"),
        State("filtro-ano", "value"),
        State("filtro-mes", "value"),
        State("filtro-cc", "value"),
        State("usuario-logado", "data"),
        prevent_initial_call=True,
    )
    def exportar_excel(n_clicks, ano, meses, cc, usuario):

        if not usuario or not ano:
            return no_update

        if meses:
            meses = [str(m).zfill(2) for m in meses]
            meses_str = "_".join(meses)
        else:
            meses_str = "todos"

        # 🔥 REGRA DEFINITIVA PARA ADMIN
        if usuario == "Admin":
            cc = None
        elif not cc:
            cc = usuario

        df = get_despesas(
            usuario=usuario,
            ano=ano,
            meses=meses,
            cc=cc
        )

        if df.empty:
            return no_update

        # 📅 Formatar Data
        if "Data" in df.columns:
            df["Data"] = pd.to_datetime(df["Data"], errors="coerce").dt.strftime("%d/%m/%Y")

        # 🧹 Remover colunas técnicas
        for col in ["Ação", "Historico"]:
            if col in df.columns:
                df = df.drop(columns=[col])

        nome_arquivo = f"despesas_{usuario}_{ano}_{meses_str}.xlsx"

        def gerar_excel(buffer):
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:

                # 📄 Aba principal
                df.to_excel(writer, sheet_name="Despesas", index=False)
                ws = writer.sheets["Despesas"]

                for cell in ws[1]:
                    cell.font = cell.font.copy(bold=True)

                for col in ws.iter_cols(min_row=2):
                    if ws[f"{col[0].column_letter}1"].value == "Realizado":
                        for cell in col:
                            cell.number_format = 'R$ #,##0.00'

                for column_cells in ws.columns:
                    length = max(len(str(cell.value)) if cell.value else 0 for cell in column_cells)
                    ws.column_dimensions[column_cells[0].column_letter].width = length + 3

                # 📊 Aba Resumo
                resumo = (
                    df.groupby("CC", dropna=False)["Realizado"]
                    .sum()
                    .reset_index()
                )

                resumo.loc[len(resumo)] = ["TOTAL GERAL", resumo["Realizado"].sum()]
                resumo.to_excel(writer, sheet_name="Resumo", index=False)

                ws_resumo = writer.sheets["Resumo"]

                for cell in ws_resumo[1]:
                    cell.font = cell.font.copy(bold=True)

                for cell in ws_resumo["B"]:
                    cell.number_format = 'R$ #,##0.00'

                ws_resumo.column_dimensions["A"].width = 30
                ws_resumo.column_dimensions["B"].width = 20

        return dcc.send_bytes(gerar_excel, nome_arquivo)