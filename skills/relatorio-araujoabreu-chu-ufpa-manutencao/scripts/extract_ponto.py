#!/usr/bin/env python3
"""
Extrai a folha de ponto (relatório de jornada) do PDF exportado pelo sistema de ponto
(ex: "Frequência_MM_AAAA.pdf") para uma estrutura JSON: um registro por colaborador por dia.

Por que por coordenadas (x0) e não por regex de texto corrido:
O PDF tem uma coluna por funcionário (uma página = um funcionário), mas o NÚMERO de colunas
numéricas impressas varia de funcionário pra funcionário (a coluna "Saldo" nem sempre aparece,
e em dias sem batida de ponto - Folga, Férias etc - as colunas de Entrada/Saída simplesmente
não são impressas, só as de totais). Por isso, extrair por posição de texto corrido (ex: "o 8º
número da linha") quebra silenciosamente. Em vez disso, localizamos a posição x de cada
cabeçalho de coluna em cada página e associamos cada valor da linha à coluna mais próxima.

Uso:
    python3 extract_ponto.py <caminho_do_pdf> [--out saida.json]
"""
import argparse
import json
import re
import sys
from pathlib import Path

import pdfplumber

DIAS_SEMANA = {"Seg,", "Ter,", "Qua,", "Qui,", "Sex,", "Sáb,", "Dom,"}

# nomes de coluna -> texto de cabeçalho usado para localizar a âncora x na página
# (a ordem aqui é só documentação; a associação real é por proximidade de x0)
COLUNAS_ANCORA = {
    "data": ["Data"],
    "1a_entrada": ["Entrada"],  # primeira ocorrência
    "1a_saida": ["Saída"],      # primeira ocorrência
    "2a_entrada": ["Entrada"],  # segunda ocorrência
    "2a_saida": ["Saída"],      # segunda ocorrência
    "credito": ["Crédito"],
    "debito": ["Débito"],
    "h_intervalo": ["H."],      # + "intervalo" logo depois
    "horas_normais": ["normais"],
    "he1": ["(50%)", "(65%)"],  # o percentual varia por regime contratual
    "he2": ["(100%)"],
    "adicional_noturno": ["noturno"],
    "saldo": ["Saldo"],         # opcional — nem toda página tem
    "motivo": ["Motivo/Observação"],
}


def build_column_anchors(header_words):
    """Recebe as palavras da linha de cabeçalho (top ~= 110) e devolve {coluna: x0}."""
    anchors = {}
    seen_entrada = 0
    seen_saida = 0
    seen_percent = 0
    for w in header_words:
        t = w["text"]
        x = w["x0"]
        if t == "Data" and "data" not in anchors:
            anchors["data"] = x
        elif t == "Entrada":
            seen_entrada += 1
            key = "1a_entrada" if seen_entrada == 1 else "2a_entrada"
            anchors[key] = x
        elif t == "Saída":
            seen_saida += 1
            key = "1a_saida" if seen_saida == 1 else "2a_saida"
            anchors[key] = x
        elif t == "Crédito":
            anchors["credito"] = x
        elif t == "Débito":
            anchors["debito"] = x
        elif t == "H." and "h_intervalo" not in anchors:
            anchors["h_intervalo"] = x
        elif t == "normais":
            anchors["horas_normais"] = x
        elif t in ("(50%)", "(65%)", "(60%)", "(70%)"):
            anchors["he1"] = x
        elif t == "(100%)":
            anchors["he2"] = x
        elif t == "noturno":
            anchors["adicional_noturno"] = x
        elif t == "Saldo":
            anchors["saldo"] = x
        elif t == "Motivo/Observação":
            anchors["motivo"] = x
    return anchors


def nearest_column(x0, anchors):
    best_col, best_dist = None, float("inf")
    for col, ax in anchors.items():
        d = abs(x0 - ax)
        if d < best_dist:
            best_dist, best_col = d, col
    return best_col


def group_lines(words, top_tol=1.2):
    """Agrupa palavras em linhas visuais pelo valor de 'top' (posição vertical)."""
    lines = []
    current, current_top = [], None
    for w in sorted(words, key=lambda w: (w["top"], w["x0"])):
        if current_top is None or abs(w["top"] - current_top) <= top_tol:
            current.append(w)
            current_top = w["top"] if current_top is None else current_top
        else:
            lines.append(current)
            current, current_top = [w], w["top"]
    if current:
        lines.append(current)
    return lines


def extract_employee_name(words):
    idx = next((i for i, w in enumerate(words) if w["text"] == "Colaborador:"), None)
    if idx is None:
        return None
    top0 = words[idx]["top"]
    name_words = [w["text"] for w in words[idx + 1:] if abs(w["top"] - top0) < 2]
    return " ".join(name_words).strip()


def parse_page(page):
    words = page.extract_words()
    nome = extract_employee_name(words)
    if not nome:
        return None

    header_words = [w for w in words if abs(w["top"] - 110.2) < 1.5]
    anchors = build_column_anchors(header_words)
    if "data" not in anchors or "motivo" not in anchors:
        # página sem tabela reconhecível — pula
        return {"colaborador": nome, "dias": [], "aviso": "cabeçalho de tabela não localizado nesta página"}

    body_words = [w for w in words if w["top"] > 111.5]
    lines = group_lines(body_words)

    dias = []
    current_row = None
    for line in lines:
        line_sorted = sorted(line, key=lambda w: w["x0"])
        first_text = line_sorted[0]["text"]

        if first_text == "TOTAIS":
            break  # fim da tabela de dias; o que vem depois é rodapé
        if first_text in ("Colaborador", "Empregador"):
            continue

        if first_text in DIAS_SEMANA:
            # nova linha de dia
            if current_row:
                dias.append(current_row)
            weekday = first_text.rstrip(",")
            date_word = line_sorted[1]["text"] if len(line_sorted) > 1 else None
            current_row = {
                "data": date_word,
                "dia_semana": weekday,
                "1a_entrada": None, "1a_saida": None,
                "2a_entrada": None, "2a_saida": None,
                "credito": None, "debito": None, "h_intervalo": None,
                "horas_normais": None, "he1": None, "he2": None,
                "adicional_noturno": None, "saldo": None,
                "motivo": "",
            }
            for w in line_sorted[2:]:
                col = nearest_column(w["x0"], anchors)
                if col == "motivo":
                    current_row["motivo"] = (current_row["motivo"] + " " + w["text"]).strip()
                elif col in ("data",):
                    continue
                else:
                    current_row[col] = w["text"]
        else:
            # possível continuação do motivo (linha sem dia da semana no início)
            leftmost_x = line_sorted[0]["x0"]
            motivo_anchor = anchors.get("motivo", 470)
            if current_row is not None and leftmost_x >= motivo_anchor - 15:
                texto = " ".join(w["text"] for w in line_sorted)
                current_row["motivo"] = (current_row["motivo"] + " " + texto).strip()
            # senão: linha não reconhecida (ex: ruído de rodapé) — ignora

    if current_row:
        dias.append(current_row)

    return {"colaborador": nome, "dias": dias}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf_path")
    ap.add_argument("--out", default=None, help="Caminho do JSON de saída (default: <pdf>.json)")
    args = ap.parse_args()

    pdf_path = Path(args.pdf_path)
    out_path = Path(args.out) if args.out else pdf_path.with_suffix(".json")

    resultado = {"arquivo_origem": pdf_path.name, "funcionarios": []}

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            parsed = parse_page(page)
            if parsed:
                resultado["funcionarios"].append(parsed)

    out_path.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: {len(resultado['funcionarios'])} funcionários extraídos -> {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
