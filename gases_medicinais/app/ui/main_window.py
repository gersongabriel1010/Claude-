"""Janela principal do aplicativo, com as abas do sistema."""
from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from app import db
from app.ui.config_tab import ConfigTab
from app.ui.context import AppContext
from app.ui.estoque_tab import EstoqueTab
from app.ui.historico_tab import HistoricoTab
from app.ui.itens_tab import ItensTab
from app.ui.movimentacao_tab import MovimentacaoTab

TITULO = "Controle de Gases Medicinais"


class MainWindow(ttk.Frame):
    def __init__(self, root: tk.Tk, db_path: Path, aviso_inicial: str | None = None):
        super().__init__(root)
        self.root = root
        root.title(TITULO)
        root.geometry("1080x680")
        root.minsize(900, 560)

        self.ctx = AppContext(db_path)
        self.pack(fill="both", expand=True)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.estoque_tab = EstoqueTab(notebook, self.ctx)
        self.movimentacao_tab = MovimentacaoTab(notebook, self.ctx)
        self.itens_tab = ItensTab(notebook, self.ctx)
        self.historico_tab = HistoricoTab(notebook, self.ctx)
        self.config_tab = ConfigTab(notebook, self.ctx)

        notebook.add(self.estoque_tab, text="Estoque Atual")
        notebook.add(self.movimentacao_tab, text="Nova Movimentação")
        notebook.add(self.itens_tab, text="Cadastro de Itens")
        notebook.add(self.historico_tab, text="Histórico")
        notebook.add(self.config_tab, text="Configurações")

        if aviso_inicial:
            self.after(200, lambda: messagebox.showwarning("Aviso", aviso_inicial))
            notebook.select(self.config_tab)


def iniciar_app(db_path: Path) -> tk.Tk:
    root = tk.Tk()
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    aviso_inicial = None
    try:
        db.init_db(db_path)
    except Exception as exc:
        aviso_inicial = (
            f"Não foi possível abrir o banco de dados configurado:\n{exc}\n\n"
            "Ajuste o caminho na aba Configurações."
        )

    MainWindow(root, db_path, aviso_inicial=aviso_inicial)
    return root
