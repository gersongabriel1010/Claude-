"""Exportação do histórico de movimentações para CSV ou Excel."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, Sequence

HEADERS = [
    "Data/Hora", "Tipo", "Item", "Quantidade", "Solicitante/Retirou",
    "Setor", "Nº Série/Patrimônio", "Responsável pelo Registro", "Observação",
]


def _row_to_values(mov) -> list:
    tipo_label = "Entrada" if mov.tipo == "ENTRADA" else "Saída"
    return [
        mov.data_hora, tipo_label, mov.item_nome, mov.quantidade,
        mov.solicitante, mov.setor, mov.numero_serie,
        mov.responsavel_registro, mov.observacao,
    ]


def export_csv(movimentacoes: Sequence, destino: Path) -> None:
    with open(destino, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(HEADERS)
        for mov in movimentacoes:
            writer.writerow(_row_to_values(mov))


def export_xlsx(movimentacoes: Sequence, destino: Path) -> None:
    from openpyxl import Workbook
    from openpyxl.styles import Font

    wb = Workbook()
    ws = wb.active
    ws.title = "Histórico de Movimentações"
    ws.append(HEADERS)
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for mov in movimentacoes:
        ws.append(_row_to_values(mov))
    for col_cells in ws.columns:
        max_len = max((len(str(c.value)) for c in col_cells if c.value is not None), default=10)
        ws.column_dimensions[col_cells[0].column_letter].width = min(max_len + 2, 40)
    wb.save(destino)
