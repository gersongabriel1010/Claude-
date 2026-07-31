"""Aba de histórico de movimentações, com filtros e exportação."""
from __future__ import annotations

import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from app import db, export
from app.ui.context import AppContext


def _parse_data_br(texto: str, fim_do_dia: bool) -> str | None:
    texto = texto.strip()
    if not texto:
        return None
    try:
        dt = datetime.strptime(texto, "%d/%m/%Y")
    except ValueError:
        raise ValueError(f"Data inválida: '{texto}'. Use o formato DD/MM/AAAA.")
    if fim_do_dia:
        dt = dt.replace(hour=23, minute=59, second=59)
    return dt.isoformat(timespec="seconds")


class HistoricoTab(ttk.Frame):
    def __init__(self, parent, ctx: AppContext):
        super().__init__(parent, padding=10)
        self.ctx = ctx
        ctx.subscribe(self._on_dados_alterados)
        self._resultados: list[db.Movimentacao] = []
        self._itens: list[db.Item] = []

        filtros = ttk.LabelFrame(self, text="Filtros", padding=10)
        filtros.pack(fill="x", pady=(0, 10))

        ttk.Label(filtros, text="Item").grid(row=0, column=0, sticky="w")
        self.var_item = tk.StringVar(value="Todos")
        self.combo_item = ttk.Combobox(filtros, textvariable=self.var_item, width=28, state="readonly")
        self.combo_item.grid(row=1, column=0, sticky="w", padx=(0, 12))

        ttk.Label(filtros, text="Tipo").grid(row=0, column=1, sticky="w")
        self.var_tipo = tk.StringVar(value="Todos")
        ttk.Combobox(filtros, textvariable=self.var_tipo, width=12, state="readonly",
                     values=["Todos", "Entrada", "Saída"]).grid(row=1, column=1, sticky="w", padx=(0, 12))

        ttk.Label(filtros, text="Data inicial (DD/MM/AAAA)").grid(row=0, column=2, sticky="w")
        self.var_data_ini = tk.StringVar()
        ttk.Entry(filtros, textvariable=self.var_data_ini, width=14).grid(row=1, column=2, sticky="w", padx=(0, 12))

        ttk.Label(filtros, text="Data final (DD/MM/AAAA)").grid(row=0, column=3, sticky="w")
        self.var_data_fim = tk.StringVar()
        ttk.Entry(filtros, textvariable=self.var_data_fim, width=14).grid(row=1, column=3, sticky="w", padx=(0, 12))

        ttk.Label(filtros, text="Solicitante").grid(row=0, column=4, sticky="w")
        self.var_solicitante = tk.StringVar()
        ttk.Entry(filtros, textvariable=self.var_solicitante, width=20).grid(row=1, column=4, sticky="w", padx=(0, 12))

        ttk.Button(filtros, text="Filtrar", command=self._filtrar).grid(row=1, column=5, sticky="w")
        ttk.Button(filtros, text="Limpar Filtros", command=self._limpar_filtros).grid(row=1, column=6, sticky="w", padx=(6, 0))

        colunas = ("data", "tipo", "item", "quantidade", "solicitante", "setor",
                   "serie", "responsavel", "observacao")
        self.tree = ttk.Treeview(self, columns=colunas, show="headings", height=16)
        titulos = {
            "data": "Data/Hora", "tipo": "Tipo", "item": "Item", "quantidade": "Qtd.",
            "solicitante": "Solicitante/Retirou", "setor": "Setor", "serie": "Nº Série/Patrim.",
            "responsavel": "Responsável Registro", "observacao": "Observação",
        }
        larguras = {"data": 130, "tipo": 70, "item": 150, "quantidade": 60, "solicitante": 130,
                    "setor": 110, "serie": 110, "responsavel": 130, "observacao": 160}
        for col in colunas:
            self.tree.heading(col, text=titulos[col])
            self.tree.column(col, width=larguras[col], anchor="center" if col in ("tipo", "quantidade") else "w")
        self.tree.pack(fill="both", expand=True)

        rodape = ttk.Frame(self)
        rodape.pack(fill="x", pady=(8, 0))
        self.label_total = ttk.Label(rodape, text="0 registro(s)")
        self.label_total.pack(side="left")
        ttk.Button(rodape, text="Exportar CSV", command=self._exportar_csv).pack(side="right", padx=(6, 0))
        ttk.Button(rodape, text="Exportar Excel", command=self._exportar_xlsx).pack(side="right")

        self._carregar_itens_filtro()
        self._filtrar()

    def _on_dados_alterados(self) -> None:
        self._carregar_itens_filtro()
        self._filtrar()

    def _carregar_itens_filtro(self) -> None:
        try:
            self._itens = db.list_itens(self.ctx.db_path, somente_ativos=False)
        except Exception as exc:
            messagebox.showerror("Erro ao carregar itens", str(exc))
            self._itens = []
        nomes = ["Todos"] + [i.nome for i in self._itens]
        self.combo_item["values"] = nomes
        if self.var_item.get() not in nomes:
            self.var_item.set("Todos")

    def _limpar_filtros(self) -> None:
        self.var_item.set("Todos")
        self.var_tipo.set("Todos")
        self.var_data_ini.set("")
        self.var_data_fim.set("")
        self.var_solicitante.set("")
        self._filtrar()

    def _filtrar(self) -> None:
        item_id = None
        if self.var_item.get() != "Todos":
            item = next((i for i in self._itens if i.nome == self.var_item.get()), None)
            item_id = item.id if item else None

        tipo_map = {"Entrada": "ENTRADA", "Saída": "SAIDA"}
        tipo = tipo_map.get(self.var_tipo.get())

        try:
            data_inicio = _parse_data_br(self.var_data_ini.get(), fim_do_dia=False)
            data_fim = _parse_data_br(self.var_data_fim.get(), fim_do_dia=True)
        except ValueError as exc:
            messagebox.showwarning("Data inválida", str(exc))
            return

        try:
            self._resultados = db.list_movimentacoes(
                self.ctx.db_path, item_id=item_id, tipo=tipo,
                data_inicio=data_inicio, data_fim=data_fim,
                solicitante=self.var_solicitante.get().strip() or None,
            )
        except Exception as exc:
            messagebox.showerror("Erro ao consultar histórico", str(exc))
            return

        for row in self.tree.get_children():
            self.tree.delete(row)
        for mov in self._resultados:
            data_fmt = mov.data_hora.replace("T", " ")
            tipo_label = "Entrada" if mov.tipo == "ENTRADA" else "Saída"
            self.tree.insert("", "end", values=(
                data_fmt, tipo_label, mov.item_nome, mov.quantidade, mov.solicitante,
                mov.setor, mov.numero_serie, mov.responsavel_registro, mov.observacao,
            ))
        self.label_total.config(text=f"{len(self._resultados)} registro(s)")

    def _exportar_csv(self) -> None:
        if not self._resultados:
            messagebox.showinfo("Nada para exportar", "Não há registros no filtro atual.")
            return
        destino = filedialog.asksaveasfilename(
            title="Exportar histórico para CSV", defaultextension=".csv",
            filetypes=[("Arquivo CSV", "*.csv")],
            initialfile="historico_movimentacoes.csv")
        if not destino:
            return
        try:
            export.export_csv(self._resultados, Path(destino))
        except Exception as exc:
            messagebox.showerror("Erro ao exportar", str(exc))
            return
        messagebox.showinfo("Exportado", f"Arquivo salvo em:\n{destino}")

    def _exportar_xlsx(self) -> None:
        if not self._resultados:
            messagebox.showinfo("Nada para exportar", "Não há registros no filtro atual.")
            return
        destino = filedialog.asksaveasfilename(
            title="Exportar histórico para Excel", defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")],
            initialfile="historico_movimentacoes.xlsx")
        if not destino:
            return
        try:
            export.export_xlsx(self._resultados, Path(destino))
        except ImportError:
            messagebox.showerror(
                "Recurso indisponível",
                "A biblioteca 'openpyxl' não está instalada. Use a exportação em CSV.")
            return
        except Exception as exc:
            messagebox.showerror("Erro ao exportar", str(exc))
            return
        messagebox.showinfo("Exportado", f"Arquivo salvo em:\n{destino}")
