"""Aba de cadastro/edição de itens controlados."""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from app import db
from app.ui.context import AppContext


class ItensTab(ttk.Frame):
    def __init__(self, parent, ctx: AppContext):
        super().__init__(parent, padding=10)
        self.ctx = ctx
        self.item_selecionado_id: int | None = None
        ctx.subscribe(self.refresh)

        # --- Lista de itens (esquerda) ---
        esquerda = ttk.Frame(self)
        esquerda.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ttk.Label(esquerda, text="Itens Cadastrados", font=("TkDefaultFont", 12, "bold")).pack(anchor="w")

        self.mostrar_inativos = tk.BooleanVar(value=False)
        ttk.Checkbutton(esquerda, text="Mostrar itens desativados",
                         variable=self.mostrar_inativos, command=self.refresh).pack(anchor="w", pady=(2, 6))

        colunas = ("nome", "categoria", "unidade", "minimo", "situacao")
        self.tree = ttk.Treeview(esquerda, columns=colunas, show="headings", height=18)
        titulos = {"nome": "Item", "categoria": "Categoria", "unidade": "Unidade",
                   "minimo": "Estoque Mínimo", "situacao": "Situação"}
        for col in colunas:
            self.tree.heading(col, text=titulos[col])
            self.tree.column(col, width=140, anchor="w" if col == "nome" else "center")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        # --- Formulário (direita) ---
        direita = ttk.LabelFrame(self, text="Cadastrar / Editar Item", padding=12)
        direita.pack(side="right", fill="y")

        ttk.Label(direita, text="Nome do equipamento *").grid(row=0, column=0, sticky="w", pady=(0, 2))
        self.var_nome = tk.StringVar()
        ttk.Entry(direita, textvariable=self.var_nome, width=32).grid(row=1, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(direita, text="Categoria *").grid(row=2, column=0, sticky="w", pady=(0, 2))
        self.var_categoria = tk.StringVar()
        ttk.Combobox(direita, textvariable=self.var_categoria, width=29,
                     values=db.CATEGORIAS_PADRAO).grid(row=3, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(direita, text="Unidade de medida *").grid(row=4, column=0, sticky="w", pady=(0, 2))
        self.var_unidade = tk.StringVar()
        ttk.Combobox(direita, textvariable=self.var_unidade, width=29,
                     values=["unidade", "cilindro", "peça", "kit"]).grid(row=5, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(direita, text="Estoque mínimo desejado *").grid(row=6, column=0, sticky="w", pady=(0, 2))
        self.var_minimo = tk.StringVar(value="0")
        ttk.Entry(direita, textvariable=self.var_minimo, width=32).grid(row=7, column=0, sticky="ew", pady=(0, 8))

        botoes = ttk.Frame(direita)
        botoes.grid(row=8, column=0, sticky="ew", pady=(10, 0))
        ttk.Button(botoes, text="Salvar Novo", command=self._salvar_novo).pack(fill="x", pady=2)
        self.btn_atualizar = ttk.Button(botoes, text="Atualizar Selecionado",
                                         command=self._atualizar_selecionado, state="disabled")
        self.btn_atualizar.pack(fill="x", pady=2)
        self.btn_alternar_ativo = ttk.Button(botoes, text="Desativar/Reativar Selecionado",
                                              command=self._alternar_ativo, state="disabled")
        self.btn_alternar_ativo.pack(fill="x", pady=2)
        ttk.Button(botoes, text="Limpar Formulário", command=self._limpar).pack(fill="x", pady=2)

        ttk.Label(direita, text="* campos obrigatórios", foreground="gray").grid(
            row=9, column=0, sticky="w", pady=(10, 0))

        self.refresh()

    def _itens_cache(self) -> list[db.Item]:
        return db.list_itens(self.ctx.db_path, somente_ativos=not self.mostrar_inativos.get())

    def refresh(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            self._itens = self._itens_cache()
        except Exception as exc:
            messagebox.showerror("Erro ao carregar itens", str(exc))
            self._itens = []
        for item in self._itens:
            situacao = "Ativo" if item.ativo else "Desativado"
            self.tree.insert("", "end", iid=str(item.id), values=(
                item.nome, item.categoria, item.unidade_medida, item.estoque_minimo, situacao))

    def _on_select(self, _event=None) -> None:
        selecao = self.tree.selection()
        if not selecao:
            self.item_selecionado_id = None
            self.btn_atualizar.config(state="disabled")
            self.btn_alternar_ativo.config(state="disabled")
            return
        item_id = int(selecao[0])
        item = next((i for i in self._itens if i.id == item_id), None)
        if not item:
            return
        self.item_selecionado_id = item.id
        self.var_nome.set(item.nome)
        self.var_categoria.set(item.categoria)
        self.var_unidade.set(item.unidade_medida)
        self.var_minimo.set(str(item.estoque_minimo))
        self.btn_atualizar.config(state="normal")
        self.btn_alternar_ativo.config(
            text="Reativar Selecionado" if not item.ativo else "Desativar Selecionado",
            state="normal")

    def _ler_formulario(self):
        nome = self.var_nome.get().strip()
        categoria = self.var_categoria.get().strip()
        unidade = self.var_unidade.get().strip()
        minimo_txt = self.var_minimo.get().strip().replace(",", ".")
        if not nome or not categoria or not unidade:
            messagebox.showwarning("Campos obrigatórios",
                                    "Preencha nome, categoria e unidade de medida.")
            return None
        try:
            minimo = float(minimo_txt) if minimo_txt else 0.0
            if minimo < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Valor inválido", "Estoque mínimo deve ser um número igual ou maior que zero.")
            return None
        return nome, categoria, unidade, minimo

    def _salvar_novo(self) -> None:
        dados = self._ler_formulario()
        if not dados:
            return
        try:
            db.add_item(self.ctx.db_path, *dados)
        except Exception as exc:
            messagebox.showerror("Erro ao salvar", str(exc))
            return
        messagebox.showinfo("Sucesso", "Item cadastrado com sucesso.")
        self._limpar()
        self.ctx.notify_data_changed()

    def _atualizar_selecionado(self) -> None:
        if self.item_selecionado_id is None:
            return
        dados = self._ler_formulario()
        if not dados:
            return
        try:
            db.update_item(self.ctx.db_path, self.item_selecionado_id, *dados)
        except Exception as exc:
            messagebox.showerror("Erro ao atualizar", str(exc))
            return
        messagebox.showinfo("Sucesso", "Item atualizado com sucesso.")
        self._limpar()
        self.ctx.notify_data_changed()

    def _alternar_ativo(self) -> None:
        if self.item_selecionado_id is None:
            return
        item = next((i for i in self._itens if i.id == self.item_selecionado_id), None)
        if not item:
            return
        try:
            db.set_item_ativo(self.ctx.db_path, item.id, not item.ativo)
        except Exception as exc:
            messagebox.showerror("Erro", str(exc))
            return
        self._limpar()
        self.ctx.notify_data_changed()

    def _limpar(self) -> None:
        self.tree.selection_remove(self.tree.selection())
        self.item_selecionado_id = None
        self.var_nome.set("")
        self.var_categoria.set("")
        self.var_unidade.set("")
        self.var_minimo.set("0")
        self.btn_atualizar.config(state="disabled")
        self.btn_alternar_ativo.config(state="disabled")
