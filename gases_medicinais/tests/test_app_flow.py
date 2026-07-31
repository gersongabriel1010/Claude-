"""Teste funcional de ponta a ponta, exercitando a interface real (Tkinter)
como um usuário faria: cadastrar item, registrar entrada/saída, conferir
estoque e histórico, e exportar CSV.

Executar com um display (real ou Xvfb):
    xvfb-run -a python3 -m pytest tests/test_app_flow.py -v
"""
import sys
import tkinter as tk
import tkinter.messagebox as messagebox
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# As telas usam tkinter.messagebox para avisos/confirmações. Em um teste
# automatizado não há usuário para clicar nesses popups (o que travaria a
# execução), então eles são substituídos por versões que não bloqueiam.
messagebox.showinfo = lambda *a, **k: None
messagebox.showwarning = lambda *a, **k: None
messagebox.showerror = lambda *a, **k: print("ERRO (messagebox):", a, k)
messagebox.askyesno = lambda *a, **k: True

from app import db
from app.ui.context import AppContext
from app.ui.estoque_tab import EstoqueTab
from app.ui.historico_tab import HistoricoTab
from app.ui.itens_tab import ItensTab
from app.ui.movimentacao_tab import MovimentacaoTab


class TestFluxoCompleto(unittest.TestCase):
    def setUp(self):
        import shutil
        self.tmp_dir = Path("/tmp/test_gases_" + self.id().split(".")[-1])
        shutil.rmtree(self.tmp_dir, ignore_errors=True)
        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.tmp_dir / "teste.db"
        db.init_db(self.db_path)
        self.root = tk.Tk()
        self.ctx = AppContext(self.db_path)

    def tearDown(self):
        self.root.destroy()

    def test_cadastrar_item(self):
        aba = ItensTab(self.root, self.ctx)
        aba.var_nome.set("Fluxômetro de Parede 15L")
        aba.var_categoria.set("Fluxômetro")
        aba.var_unidade.set("unidade")
        aba.var_minimo.set("5")
        aba._salvar_novo()

        itens = db.list_itens(self.db_path)
        self.assertEqual(len(itens), 1)
        self.assertEqual(itens[0].nome, "Fluxômetro de Parede 15L")
        self.assertEqual(itens[0].estoque_minimo, 5)

    def test_registrar_entrada_e_saida_atualiza_estoque(self):
        item_id = db.add_item(self.db_path, "Manômetro O2", "Manômetro", "unidade", 3)
        self.ctx.notify_data_changed()

        mov_tab = MovimentacaoTab(self.root, self.ctx)
        mov_tab.var_tipo.set("ENTRADA")
        mov_tab.combo_item.current(0)
        mov_tab.var_quantidade.set("10")
        mov_tab.var_solicitante.set("Almoxarifado Central")
        mov_tab.var_setor.set("Fornecedor XPTO")
        mov_tab.var_responsavel.set("Maria Silva")
        mov_tab._registrar()

        saldo = db.estoque_atual(self.db_path)[item_id]
        self.assertEqual(saldo, 10)

        mov_tab.var_tipo.set("SAIDA")
        mov_tab.combo_item.current(0)
        mov_tab.var_quantidade.set("4")
        mov_tab.var_solicitante.set("Enfermeiro João")
        mov_tab.var_setor.set("UTI Adulto")
        mov_tab.var_responsavel.set("Maria Silva")
        mov_tab._registrar()

        saldo = db.estoque_atual(self.db_path)[item_id]
        self.assertEqual(saldo, 6)

        movs = db.list_movimentacoes(self.db_path, item_id=item_id)
        self.assertEqual(len(movs), 2)

    def test_estoque_abaixo_do_minimo_destacado(self):
        item_id = db.add_item(self.db_path, "Regulador de Cilindro", "Regulador de Cilindro", "unidade", 5)
        db.add_movimentacao(self.db_path, "ENTRADA", item_id, 2, "Fulano", "Depósito",
                             "", "Maria Silva", "")
        self.ctx.notify_data_changed()

        estoque_tab = EstoqueTab(self.root, self.ctx)
        valores = estoque_tab.tree.item(estoque_tab.tree.get_children()[0])["values"]
        status = valores[-1]
        self.assertEqual(status, "ABAIXO DO MÍNIMO")
        tags = estoque_tab.tree.item(estoque_tab.tree.get_children()[0])["tags"]
        self.assertIn("abaixo_minimo", tags)

    def test_historico_com_filtros_e_exportacao_csv(self):
        item_id = db.add_item(self.db_path, "Cilindro de O2", "Cilindro", "unidade", 2)
        db.add_movimentacao(self.db_path, "ENTRADA", item_id, 20, "Fornecedor A", "Depósito Central",
                             "SN-001", "Maria Silva", "Compra mensal")
        db.add_movimentacao(self.db_path, "SAIDA", item_id, 3, "Téc. Carlos", "Pronto Socorro",
                             "", "Maria Silva", "Uso emergencial")
        self.ctx.notify_data_changed()

        hist_tab = HistoricoTab(self.root, self.ctx)
        hist_tab._filtrar()
        self.assertEqual(len(hist_tab._resultados), 2)

        hist_tab.var_tipo.set("Saída")
        hist_tab._filtrar()
        self.assertEqual(len(hist_tab._resultados), 1)
        self.assertEqual(hist_tab._resultados[0].setor, "Pronto Socorro")

        from app import export
        destino_csv = self.tmp_dir / "export.csv"
        export.export_csv(hist_tab._resultados, destino_csv)
        self.assertTrue(destino_csv.exists())
        conteudo = destino_csv.read_text(encoding="utf-8-sig")
        self.assertIn("Pronto Socorro", conteudo)

        destino_xlsx = self.tmp_dir / "export.xlsx"
        export.export_xlsx(hist_tab._resultados, destino_xlsx)
        self.assertTrue(destino_xlsx.exists())

    def test_historico_atualiza_sozinho_quando_movimentacao_e_criada_em_outra_aba(self):
        item_id = db.add_item(self.db_path, "Valvula de Fluxo", "Válvula", "unidade", 1)
        self.ctx.notify_data_changed()

        hist_tab = HistoricoTab(self.root, self.ctx)
        self.assertEqual(len(hist_tab._resultados), 0)

        mov_tab = MovimentacaoTab(self.root, self.ctx)
        mov_tab.var_tipo.set("ENTRADA")
        mov_tab.combo_item.current(0)
        mov_tab.var_quantidade.set("7")
        mov_tab.var_solicitante.set("Fulano")
        mov_tab.var_setor.set("Depósito")
        mov_tab.var_responsavel.set("Maria Silva")
        mov_tab._registrar()

        self.assertEqual(len(hist_tab._resultados), 1)
        self.assertEqual(hist_tab._resultados[0].item_id, item_id)

    def test_desativar_item_some_do_combo_de_movimentacao(self):
        item_id = db.add_item(self.db_path, "Item Antigo", "Outro", "unidade", 0)
        self.ctx.notify_data_changed()
        mov_tab = MovimentacaoTab(self.root, self.ctx)
        self.assertEqual(len(mov_tab._itens_ativos), 1)

        db.set_item_ativo(self.db_path, item_id, False)
        self.ctx.notify_data_changed()
        self.assertEqual(len(mov_tab._itens_ativos), 0)


if __name__ == "__main__":
    unittest.main()
