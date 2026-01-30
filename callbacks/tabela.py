from dash import Input, Output, State, html, dash_table, ctx, dcc, no_update
import dash_bootstrap_components as dbc
import pandas as pd

from services.despesas_service import get_despesas


def registrar_tabela_callbacks(app):

    # ================================
    # 📋 ATUALIZAÇÃO DA TABELA PRINCIPAL
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

        # Ajustar meses
        if meses:
            meses = [str(m).zfill(2) for m in meses]

        # Buscar dados do banco
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

        # ✅ Garantir que Descricao existe
        if "Descricao" not in df.columns:
            df["Descricao"] = "SEM DESCRIÇÃO"

        # 🔍 Criar botão Ação
        df["Ação"] = "🔍 Ver Detalhes"

        # 💰 Total Geral
        total = df["Realizado"].sum()

        # ============================
        # ✅ TABELA PRINCIPAL
        # ============================
        tabela = dash_table.DataTable(
            id="datatable-despesas",
            columns=[
                {"name": "CC", "id": "CC"},
                {"name": "Descricao", "id": "Descricao"},

                # 🔥 Colunas ocultas (usadas no modal)
                # {"name": "Conta", "id": "Conta", "hidden": True},
                # {"name": "Descrição Conta", "id": "Descrição Conta", "hidden": True},
                #{"name": "Historico", "id": "Historico", "hidden": True},

                {
                    "name": "Realizado (R$)",
                    "id": "Realizado",
                    "type": "numeric",
                    "format": {"specifier": ",.2f"},
                },
                {"name": "Data", "id": "Data"},
                {
                    "name": "Ação",
                    "id": "Ação",
                    "presentation": "markdown",
                },
            ],
            data=df.to_dict("records"),
            page_size=15,

            style_table={"overflowX": "auto"},

            style_cell={
                "padding": "8px",
                "fontFamily": "Arial",
                "fontSize": "14px",
                "textAlign": "left",
            },

            style_header={
                "backgroundColor": "#f0f0f0",
                "fontWeight": "bold",
                "textAlign": "center",
            },
        )

        # ============================
        # 📄 MODAL (Detalhes)
        # ============================
        modal = dbc.Modal(
            [
                dbc.ModalBody(id="modal-historico-body"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Fechar",
                        id="fechar-modal-historico",
                        color="secondary",
                    )
                ),
            ],
            id="modal-historico",
            is_open=False,
            size="xl",
            centered=True,
            scrollable=True,
        )

        return html.Div(
            [
                html.H5(
                    f"💰 Total Geral: R$ {total:,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", "."),
                    style={
                        "textAlign": "center",
                        "marginBottom": "15px",
                        "fontWeight": "600",
                    },
                ),
                tabela,
                modal,
            ]
        )

    # ================================
    # 📄 MODAL DETALHADO (Ver Detalhes)
    # ================================
    @app.callback(
        Output("modal-historico", "is_open"),
        Output("modal-historico-body", "children"),
        Input("datatable-despesas", "active_cell"),
        Input("fechar-modal-historico", "n_clicks"),
        State("datatable-despesas", "data"),
        State("modal-historico", "is_open"),
        prevent_initial_call=True,
    )
    def abrir_modal(active_cell, fechar, rows, is_open):

        # 🔒 Fechar modal
        if ctx.triggered_id == "fechar-modal-historico":
            return False, html.Div()

        # 🔒 Se não clicou em nada
        if not active_cell:
            return is_open, no_update

        # 🔥 Só abre se clicar na coluna Ação
        if active_cell["column_id"] != "Ação":
            return is_open, no_update

        # 📌 Registro clicado
        registro = rows[active_cell["row"]]

        conta = registro.get("Conta", "N/A")
        descricao_conta = registro.get("Descrição Conta", "N/A")
        historico = registro.get("Historico", "Sem histórico disponível")

        # ============================
        # ✅ Conteúdo Modal
        # ============================
        conteudo = html.Div(
            [
                html.H4(
                    "📄 Detalhes da Despesa",
                    style={
                        "textAlign": "center",
                        "fontWeight": "600",
                        "marginBottom": "20px",
                    },
                ),

                dash_table.DataTable(
                    columns=[
                        {"name": "Conta", "id": "Conta"},
                        {"name": "Descrição Conta", "id": "Descrição Conta"},
                        {"name": "Histórico", "id": "Historico"},
                    ],
                    data=[
                        {
                            "Conta": conta,
                            "Descrição Conta": descricao_conta,
                            "Historico": historico,
                        }
                    ],
                    style_table={
                        "overflowX": "auto",
                        "width": "100%",
                    },
                    style_cell={
                        "padding": "10px",
                        "fontFamily": "Arial",
                        "fontSize": "14px",
                        "textAlign": "left",
                        "whiteSpace": "normal",
                        "height": "auto",
                    },
                    style_header={
                        "backgroundColor": "#f0f0f0",
                        "fontWeight": "bold",
                        "textAlign": "center",
                    },
                ),
            ]
        )

        return True, conteudo

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

        # Ajustar meses
        if meses:
            meses = [str(m).zfill(2) for m in meses]
            meses_str = "_".join(meses)
        else:
            meses_str = "todos"

        # Buscar dados
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

        # Garantir descrição
        if "Descricao" not in df.columns:
            df["Descricao"] = "SEM DESCRIÇÃO"

        # Exportar somente colunas principais
        df = df[["CC", "Descricao", "Realizado", "Data"]]

        nome_arquivo = f"despesas_{usuario}_{ano}_{meses_str}.xlsx"

        def gerar_excel(buffer):
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:

                df.to_excel(writer, sheet_name="Despesas", index=False)
                ws = writer.sheets["Despesas"]

                # Cabeçalho bold
                for cell in ws[1]:
                    cell.font = cell.font.copy(bold=True)

                # Ajustar largura automática
                for column_cells in ws.columns:
                    length = max(len(str(cell.value)) if cell.value else 0 for cell in column_cells)
                    ws.column_dimensions[column_cells[0].column_letter].width = length + 3

        return dcc.send_bytes(gerar_excel, nome_arquivo)