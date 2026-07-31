"""Aba de configuração do local do banco de dados."""
from __future__ import annotations

from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from app import config as app_config
from app import db
from app.ui.context import AppContext


class ConfigTab(ttk.Frame):
    def __init__(self, parent, ctx: AppContext):
        super().__init__(parent, padding=16)
        self.ctx = ctx

        ttk.Label(self, text="Configuração do Banco de Dados",
                  font=("TkDefaultFont", 13, "bold")).pack(anchor="w", pady=(0, 12))

        ttk.Label(self, text=(
            "O banco de dados é um único arquivo (.db). Para que todos os "
            "computadores do setor vejam os mesmos dados, aponte esse "
            "caminho para uma pasta de rede compartilhada (ex.: um HD de "
            "rede ou uma unidade mapeada, tipo Z:\\Gases\\gases_medicinais.db).\n\n"
            "Configure o MESMO arquivo em todos os computadores que forem usar o programa."
        ), wraplength=640, justify="left").pack(anchor="w", pady=(0, 16))

        caixa = ttk.LabelFrame(self, text="Caminho atual do arquivo de banco de dados", padding=12)
        caixa.pack(fill="x", pady=(0, 16))
        self.label_caminho = ttk.Label(caixa, text=str(self.ctx.db_path), foreground="#1a5276")
        self.label_caminho.pack(anchor="w")

        botoes = ttk.Frame(self)
        botoes.pack(anchor="w", pady=(0, 16))
        ttk.Button(botoes, text="Criar novo banco em uma pasta...",
                   command=self._criar_novo).pack(side="left", padx=(0, 8))
        ttk.Button(botoes, text="Usar banco existente (arquivo .db)...",
                   command=self._usar_existente).pack(side="left", padx=(0, 8))
        ttk.Button(botoes, text="Testar Conexão", command=self._testar_conexao).pack(side="left")

        self.label_status = ttk.Label(self, text="", foreground="green")
        self.label_status.pack(anchor="w")

        ttk.Separator(self).pack(fill="x", pady=16)
        ttk.Label(self, text=(
            "Dica: na primeira instalação em um hospital, escolha "
            "'Criar novo banco em uma pasta...' apontando para a pasta de "
            "rede compartilhada. Nos demais computadores, escolha 'Usar "
            "banco existente' e selecione esse mesmo arquivo pela rede."
        ), wraplength=640, justify="left", foreground="gray").pack(anchor="w")

    def _criar_novo(self) -> None:
        pasta = filedialog.askdirectory(title="Selecione a pasta onde o banco de dados será criado")
        if not pasta:
            return
        novo_caminho = Path(pasta) / app_config.DEFAULT_DB_FILE_NAME
        self._aplicar_caminho(novo_caminho)

    def _usar_existente(self) -> None:
        arquivo = filedialog.askopenfilename(
            title="Selecione o arquivo de banco de dados existente (.db)",
            filetypes=[("Banco de dados SQLite", "*.db"), ("Todos os arquivos", "*.*")])
        if not arquivo:
            return
        self._aplicar_caminho(Path(arquivo))

    def _aplicar_caminho(self, novo_caminho: Path) -> None:
        try:
            db.init_db(novo_caminho)
        except Exception as exc:
            messagebox.showerror("Erro ao configurar banco de dados", str(exc))
            return
        app_config.set_db_path(novo_caminho)
        self.ctx.set_db_path(novo_caminho)
        self.label_caminho.config(text=str(novo_caminho))
        self.label_status.config(text="Caminho atualizado com sucesso.", foreground="green")
        messagebox.showinfo("Sucesso", f"O programa agora usará o banco de dados em:\n{novo_caminho}")

    def _testar_conexao(self) -> None:
        try:
            db.init_db(self.ctx.db_path)
            itens = db.list_itens(self.ctx.db_path)
        except Exception as exc:
            self.label_status.config(text=f"Falha na conexão: {exc}", foreground="red")
            return
        self.label_status.config(
            text=f"Conexão OK. {len(itens)} item(ns) cadastrado(s) neste banco.", foreground="green")
