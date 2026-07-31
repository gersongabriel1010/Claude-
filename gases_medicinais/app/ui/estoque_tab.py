"""Aba de visualização do estoque atual."""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from app import db
from app.ui.context import AppContext


def _formatar_qtd(valor: float) -> str:
    if float(valor).is_integer():
        return str(int(valor))
    return f"{valor:.2f}".rstrip("0").rstrip(".")


class EstoqueTab(ttk.Frame):
    def __init__(self, parent, ctx: AppContext):
        super().__init__(parent, padding=10)
        self.ctx = ctx
        ctx.subscribe(self.refresh)

        topo = ttk.Frame(self)
        topo.pack(fill="x", pady=(0, 8))
        ttk.Label(topo, text="Estoque Atual", font=("TkDefaultFont", 13, "bold")).pack(side="left")
        ttk.Button(topo, text="Atualizar", command=self.refresh).pack(side="right")

        legenda = ttk.Frame(self)
        legenda.pack(fill="x", pady=(0, 6))
        aviso = tk.Label(legenda, text="  ", bg="#f4b6b6")
        aviso.pack(side="left")
        ttk.Label(legenda, text=" Abaixo do estoque mínimo").pack(side="left")

        colunas = ("nome", "categoria", "unidade", "atual", "minimo", "status")
        self.tree = ttk.Treeview(self, columns=colunas, show="headings", height=18)
        titulos = {
            "nome": "Item", "categoria": "Categoria", "unidade": "Unidade",
            "atual": "Estoque Atual", "minimo": "Estoque Mínimo", "status": "Situação",
        }
        larguras = {"nome": 220, "categoria": 150, "unidade": 100, "atual": 110,
                    "minimo": 110, "status": 130}
        for col in colunas:
            self.tree.heading(col, text=titulos[col])
            self.tree.column(col, width=larguras[col], anchor="center" if col != "nome" else "w")
        self.tree.tag_configure("abaixo_minimo", background="#f4b6b6")
        self.tree.pack(fill="both", expand=True)

        self.refresh()

    def refresh(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            itens = db.list_itens(self.ctx.db_path, somente_ativos=True)
            saldos = db.estoque_atual(self.ctx.db_path)
        except Exception as exc:
            messagebox.showerror("Erro ao carregar estoque", str(exc))
            return
        for item in itens:
            saldo = saldos.get(item.id, 0)
            abaixo = saldo < item.estoque_minimo
            status = "ABAIXO DO MÍNIMO" if abaixo else "Normal"
            tags = ("abaixo_minimo",) if abaixo else ()
            self.tree.insert("", "end", values=(
                item.nome, item.categoria, item.unidade_medida,
                _formatar_qtd(saldo), _formatar_qtd(item.estoque_minimo), status,
            ), tags=tags)
