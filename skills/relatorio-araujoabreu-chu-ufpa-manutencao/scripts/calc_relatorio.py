#!/usr/bin/env python3
"""
Consolida os 3 indicadores do IMR (Instrumento de Medição de Resultados) do contrato,
calcula o VDT (Percentual Total de Desconto Mensal) e o valor final devido no mês.

Recebe um único JSON de entrada com os dados que o fiscal informa manualmente todo mês
(ver dados_mes.exemplo.json neste diretório) e devolve um JSON consolidado, pronto pra
alimentar o gerador do relatório em .docx (gerar_docx.js).

Uso:
    python3 calc_relatorio.py dados_mes.json --out relatorio_final.json
"""
import argparse
import json
import sys
from pathlib import Path


def faixa_indicador_1_2(percentual):
    """Indicadores 1 (RC) e 2 (PMP) usam a mesma régua de faixas."""
    if percentual >= 93:
        return {"desconto_pct": 0, "sancao": None, "atendeu_meta": True}
    if percentual >= 85:
        return {"desconto_pct": 2, "sancao": "Advertência", "atendeu_meta": False}
    return {"desconto_pct": 5, "sancao": "Advertência e Multa", "atendeu_meta": False}


def faixa_indicador_3(percentual):
    if percentual >= 98:
        return {"desconto_pct": 0, "sancao": None, "atendeu_meta": True, "rescisao": False}
    if percentual >= 95:
        return {"desconto_pct": 5, "sancao": None, "atendeu_meta": False, "rescisao": False}
    if percentual >= 90:
        return {"desconto_pct": 10, "sancao": None, "atendeu_meta": False, "rescisao": False}
    return {"desconto_pct": 20, "sancao": None, "atendeu_meta": False, "rescisao": True}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dados_mes_json")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    dados = json.loads(Path(args.dados_mes_json).read_text(encoding="utf-8"))

    # --- Indicador 1: RC ---
    ncc = dados["indicador1"]["ncc_chamados_corretivos_totais"]
    nmc = dados["indicador1"]["nmc_manutencoes_corretivas_realizadas"]
    rc = round((nmc / ncc) * 100, 2) if ncc else None
    faixa1 = faixa_indicador_1_2(rc)

    # --- Indicador 2: PMP ---
    mp = dados["indicador2"]["mp_servicos_planejados"]
    me = dados["indicador2"]["me_servicos_executados"]
    pmp = round((me / mp) * 100, 2) if mp else None
    faixa2 = faixa_indicador_1_2(pmp)

    # --- Indicador 3: DSC (já calculado por calc_indicador3.py, aqui só usamos o final revisado) ---
    ind3 = dados["indicador3"]
    horas_dia = ind3["horas_trabalho_dia"]
    qtd_func = ind3["quantidade_funcionarios"]
    dias_uteis = ind3["dias_uteis_no_mes"]
    faltas_final = ind3["total_faltas_final_revisado"]  # número que o fiscal decidiu após revisar a lista
    hpr = round(horas_dia * qtd_func * dias_uteis, 2)
    ht = round(hpr - (faltas_final * horas_dia), 2)
    dsc = round((ht / hpr) * 100, 2) if hpr else None
    faixa3 = faixa_indicador_3(dsc)

    # --- VDT: soma dos percentuais de desconto dos 3 indicadores ---
    vdt_pct = faixa1["desconto_pct"] + faixa2["desconto_pct"] + faixa3["desconto_pct"]

    # --- Valor da mão de obra, com desconto por vaga não substituída (se houver) ---
    valor_mao_obra_base = dados["mao_de_obra"]["valor_mensal_base"]
    descontos_vaga = dados["mao_de_obra"].get("descontos_vaga_nao_substituida", [])
    total_desconto_vaga = 0.0
    detalhe_descontos_vaga = []
    for dv in descontos_vaga:
        valor_cargo_mensal = dv["valor_mensal_do_cargo"]
        dias_sem_substituto = dv["dias_sem_substituto"]
        desconto = round(valor_cargo_mensal * (dias_sem_substituto / dias_uteis), 2)
        total_desconto_vaga += desconto
        detalhe_descontos_vaga.append({**dv, "valor_descontado": desconto})

    valor_mao_obra_apos_vdt = round(valor_mao_obra_base * (1 - vdt_pct / 100), 2)
    valor_mao_obra_final = round(valor_mao_obra_apos_vdt - total_desconto_vaga, 2)

    # --- OF/OS ---
    ofs_os = dados.get("of_os", [])
    total_of_os = round(sum(item["valor"] for item in ofs_os), 2)

    valor_total_mes = round(valor_mao_obra_final + total_of_os, 2)

    saida = {
        "identificacao": dados.get("identificacao", {}),
        "indicador1_rc": {
            "ncc": ncc, "nmc": nmc, "resultado_percentual": rc, **faixa1,
        },
        "indicador2_pmp": {
            "mp": mp, "me": me, "resultado_percentual": pmp, **faixa2,
        },
        "indicador3_dsc": {
            "horas_trabalho_dia": horas_dia, "quantidade_funcionarios": qtd_func,
            "dias_uteis_no_mes": dias_uteis, "total_faltas_considerado": faltas_final,
            "HPR": hpr, "HT": ht, "resultado_percentual": dsc, **faixa3,
        },
        "vdt_percentual_total_desconto": vdt_pct,
        "mao_de_obra": {
            "valor_base": valor_mao_obra_base,
            "apos_vdt": valor_mao_obra_apos_vdt,
            "descontos_vaga_nao_substituida": detalhe_descontos_vaga,
            "total_desconto_vaga": round(total_desconto_vaga, 2),
            "valor_final": valor_mao_obra_final,
        },
        "of_os": ofs_os,
        "total_of_os": total_of_os,
        "valor_total_do_mes": valor_total_mes,
        "alertas": [],
    }

    if faixa3.get("rescisao"):
        saida["alertas"].append(
            "ATENÇÃO: DSC abaixo de 90% — a faixa de ajuste prevê desconto de 20% + possível "
            "RESCISÃO CONTRATUAL. Confirme esse resultado manualmente antes de enviar o relatório."
        )
    if faixa1["sancao"] or faixa2["sancao"]:
        saida["alertas"].append(
            "Há indicador(es) fora da meta com sanção administrativa prevista (advertência e/ou "
            "multa) — confira o texto de sanções no relatório final."
        )

    out_path = Path(args.out) if args.out else Path(args.dados_mes_json).with_name("relatorio_final.json")
    out_path.write_text(json.dumps(saida, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK -> {out_path}", file=sys.stderr)
    print(f"RC={rc}% | PMP={pmp}% | DSC={dsc}% | VDT={vdt_pct}% | Valor total do mês: R$ {valor_total_mes:,.2f}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
