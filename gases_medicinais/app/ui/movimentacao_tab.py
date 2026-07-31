"""Aba de registro de entrada/saída de materiais."""
from __future__ import annotations

import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from app import db
from app.ui.context import AppContext


class MovimentacaoTab(ttk.Frame):
    def __init__(self, parent, ctx: AppContext):
        super().__init__(parent, padding=16)
        self.ctx = ctx
        ctx.subscribe(self._on_dados_alterados_externamente)
        self._itens_ativos: list[db.Item] = []

        ttk.Label(self, text="Registrar Entrada / Saída de Material",
                  font=("TkDefaultFont", 13, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        linha = 1

        ttk.Label(self, text="Tipo de movimentação *").grid(row=linha, column=0, sticky="w")
        self.var_tipo = tk.StringVar(value="ENTRADA")
        frame_tipo = ttk.Frame(self)
        frame_tipo.grid(row=linha, column=1, sticky="w")
        ttk.Radiobutton(frame_tipo, text="Entrada", variable=self.var_tipo, value="ENTRADA",
                         command=self._atualizar_rotulo_setor).pack(side="left", padx=(0, 12))
        ttk.Radiobutton(frame_tipo, text="Saída", variable=self.var_tipo, value="SAIDA",
                         command=self._atualizar_rotulo_setor).pack(side="left")
        linha += 1

        ttk.Label(self, text="Item *").grid(row=linha, column=0, sticky="w", pady=(10, 0))
        self.var_item = tk.StringVar()
        self.combo_item = ttk.Combobox(self, textvariable=self.var_item, width=45, state="readonly")
        self.combo_item.grid(row=linha, column=1, sticky="w", pady=(10, 0))
        linha += 1

        ttk.Label(self, text="Quantidade *").grid(row=linha, column=0, sticky="w", pady=(10, 0))
        self.var_quantidade = tk.StringVar()
        ttk.Entry(self, textvariable=self.var_quantidade, width=20).grid(row=linha, column=1, sticky="w", pady=(10, 0))
        linha += 1

        ttk.Label(self, text="Quem solicitou/retirou *").grid(row=linha, column=0, sticky="w", pady=(10, 0))
        self.var_solicitante = tk.StringVar()
        self.combo_solicitante = ttk.Combobox(self, textvariable=self.var_solicitante, width=45)
        self.combo_solicitante.grid(row=linha, column=1, sticky="w", pady=(10, 0))
        linha += 1

        self.label_setor = ttk.Label(self, text="Setor de destino")
        self.label_setor.grid(row=linha, column=0, sticky="w", pady=(10, 0))
        self.var_setor = tk.StringVar()
        self.combo_setor = ttk.Combobox(self, textvariable=self.var_setor, width=45)
        self.combo_setor.grid(row=linha, column=1, sticky="w", pady=(10, 0))
        linha += 1

        ttk.Label(self, text="Nº de série / patrimônio (opcional)").grid(row=linha, column=0, sticky="w", pady=(10, 0))
        self.var_serie = tk.StringVar()
        ttk.Entry(self, textvariable=self.var_serie, width=45).grid(row=linha, column=1, sticky="w", pady=(10, 0))
        linha += 1

        ttk.Label(self, text="Responsável pelo registro *").grid(row=linha, column=0, sticky="w", pady=(10, 0))
        self.var_responsavel = tk.StringVar()
        self.combo_responsavel = ttk.Combobox(self, textvariable=self.var_responsavel, width=45)
        self.combo_responsavel.grid(row=linha, column=1, sticky="w", pady=(10, 0))
        linha += 1

        ttk.Label(self, text="Data/hora (automática)").grid(row=linha, column=0, sticky="w", pady=(10, 0))
        self.label_data_hora = ttk.Label(self, text="")
        self.label_data_hora.grid(row=linha, column=1, sticky="w", pady=(10, 0))
        linha += 1

        ttk.Label(self, text="Observação").grid(row=linha, column=0, sticky="nw", pady=(10, 0))
        self.texto_obs = tk.Text(self, width=45, height=4)
        self.texto_obs.grid(row=linha, column=1, sticky="w", pady=(10, 0))
        linha += 1

        ttk.Button(self, text="Registrar Movimentação", command=self._registrar).grid(
            row=linha, column=1, sticky="w", pady=(16, 0))

        ttk.Label(self, text="* campos obrigatórios", foreground="gray").grid(
            row=linha + 1, column=1, sticky="w", pady=(4, 0))

        self._atualizar_rotulo_setor()
        self._atualizar_relogio()
        self._carregar_listas()

    def _atualizar_relogio(self) -> None:
        self.label_data_hora.config(text=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        self.after(1000, self._atualizar_relogio)

    def _atualizar_rotulo_setor(self) -> None:
        if self.var_tipo.get() == "ENTRADA":
            self.label_setor.config(text="Setor/fornecedor de origem")
        else:
            self.label_setor.config(text="Setor de destino *")

    def _on_dados_alterados_externamente(self) -> None:
        self._carregar_listas()

    def _carregar_listas(self) -> None:
        try:
            self._itens_ativos = db.list_itens(self.ctx.db_path, somente_ativos=True)
            self.combo_item["values"] = [f"{i.nome} ({i.categoria})" for i in self._itens_ativos]
            self.combo_solicitante["values"] = db.list_distinct_values(self.ctx.db_path, "solicitante")
            self.combo_responsavel["values"] = db.list_distinct_values(self.ctx.db_path, "responsavel_registro")
            self.combo_setor["values"] = db.list_distinct_values(self.ctx.db_path, "setor")
        except Exception as exc:
            messagebox.showerror("Erro ao carregar dados", str(exc))

    def _registrar(self) -> None:
        if not self._itens_ativos:
            messagebox.showwarning("Nenhum item cadastrado",
                                    "Cadastre ao menos um item na aba 'Cadastro de Itens' antes de registrar movimentações.")
            return
        indice = self.combo_item.current()
        if indice < 0:
            messagebox.showwarning("Item obrigatório", "Selecione o item.")
            return
        item = self._itens_ativos[indice]

        qtd_txt = self.var_quantidade.get().strip().replace(",", ".")
        try:
            quantidade = float(qtd_txt)
            if quantidade <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Quantidade inválida", "Informe uma quantidade numérica maior que zero.")
            return

        solicitante = self.var_solicitante.get().strip()
        responsavel = self.var_responsavel.get().strip()
        tipo = self.var_tipo.get()
        setor = self.var_setor.get().strip()

        if not solicitante:
            messagebox.showwarning("Campo obrigatório", "Informe quem solicitou/retirou o material.")
            return
        if not responsavel:
            messagebox.showwarning("Campo obrigatório", "Informe o responsável pelo registro.")
            return
        if tipo == "SAIDA" and not setor:
            messagebox.showwarning("Campo obrigatório", "Informe o setor de destino da saída.")
            return

        if tipo == "SAIDA":
            try:
                saldo_atual = db.estoque_atual(self.ctx.db_path).get(item.id, 0)
            except Exception as exc:
                messagebox.showerror("Erro ao consultar estoque", str(exc))
                return
            if quantidade > saldo_atual:
                prosseguir = messagebox.askyesno(
                    "Estoque insuficiente",
                    f"O estoque atual de '{item.nome}' é {saldo_atual}, menor que a "
                    f"quantidade de saída informada ({quantidade}).\n\n"
                    "Deseja registrar mesmo assim?",
                )
                if not prosseguir:
                    return

        observacao = self.texto_obs.get("1.0", "end").strip()

        try:
            db.add_movimentacao(
                self.ctx.db_path, tipo=tipo, item_id=item.id, quantidade=quantidade,
                solicitante=solicitante, setor=setor, numero_serie=self.var_serie.get().strip(),
                responsavel_registro=responsavel, observacao=observacao,
            )
        except Exception as exc:
            messagebox.showerror("Erro ao registrar movimentação", str(exc))
            return

        messagebox.showinfo("Sucesso", "Movimentação registrada com sucesso.")
        self._limpar_formulario()
        self.ctx.notify_data_changed()

    def _limpar_formulario(self) -> None:
        self.var_quantidade.set("")
        self.var_serie.set("")
        self.var_setor.set("")
        self.texto_obs.delete("1.0", "end")
        self.combo_item.set("")
