#!/usr/bin/env python3
"""
A partir do JSON gerado por extract_ponto.py, calcula:
  1) os dias úteis do mês (seg-sex, excluindo feriados nacionais/estaduais/municipais de Belém-PA)
  2) a lista de faltas (cheias) e meias-faltas por colaborador, com data e motivo
  3) o indicador 3 (DSC) conforme a fórmula do IMR:
       HPR = horas_dia * qtd_funcionarios * dias_uteis
       HT  = HPR - (total_faltas_em_dias * horas_dia)
       DSC = HT / HPR * 100

Regras de negócio (confirmadas com o usuário):
  - Dia útil = segunda a sexta, exceto feriados nacionais/estaduais/municipais (fonte:
    references/feriados_belem.json). Pontos facultativos federais só entram se
    --incluir-pontos-facultativos for passado (não entram por padrão).
  - Falta cheia (1,0): horas_normais == 00:00 num dia útil, qualquer que seja o motivo
    (atestado médico, licença, liberação do cliente etc. contam igual).
  - Meia falta (0,5): 00:00 < horas_normais < 06:00 num dia útil, qualquer que seja o motivo.
  - Sábado/Domingo e feriados nunca contam, mesmo que o motivo diga algo diferente.

O total de faltas calculado aqui é uma SUGESTÃO para revisão manual — o fiscal decide o
número final que entra na fórmula do indicador (ver campo "faltas_sugeridas" vs. o que for
efetivamente usado).

Uso:
    python3 calc_indicador3.py <ponto_extraido.json> --mes 7 --ano 2026 \
        [--feriados feriados_belem.json] [--horas-dia 8.8] [--qtd-funcionarios 27] \
        [--employee-list lista_funcionarios.json] [--out indicador3.json]
"""
import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

DIA_SEMANA_UTIL = {"Seg", "Ter", "Qua", "Qui", "Sex"}


def parse_hhmm_to_minutes(s):
    """Converte 'HH:MM' (ou 'HH:MMp', '-HH:MM' etc.) em minutos. None/vazio -> None."""
    if not s:
        return None
    s = s.strip()
    neg = s.startswith("-")
    s = s.lstrip("-")
    m = re.match(r"(\d{1,3}):(\d{2})", s)  # tolera sufixos como 'p' colados (ver observação no README)
    if not m:
        return None
    h, mm = int(m.group(1)), int(m.group(2))
    total = h * 60 + mm
    return -total if neg else total


def carrega_feriados(path_json, ano, incluir_pontos_facultativos=False):
    data = json.loads(Path(path_json).read_text(encoding="utf-8"))
    ano_data = data.get(str(ano))
    if not ano_data:
        raise ValueError(f"Não há calendário de feriados cadastrado para o ano {ano} em {path_json}. "
                          f"Atualize references/feriados_belem.json antes de continuar.")
    feriados = set()
    origem = {}
    grupos = ["feriados_nacionais", "feriados_estaduais_pa", "feriados_municipais_belem"]
    if incluir_pontos_facultativos:
        grupos.append("pontos_facultativos_federais")
    for grupo in grupos:
        for item in ano_data.get(grupo, []):
            feriados.add(item["data"])
            origem[item["data"]] = item["nome"]
    return feriados, origem


def dias_uteis_do_mes(mes, ano, feriados_set):
    primeiro = date(ano, mes, 1)
    if mes == 12:
        proximo_mes = date(ano + 1, 1, 1)
    else:
        proximo_mes = date(ano, mes + 1, 1)
    dias = []
    d = primeiro
    while d < proximo_mes:
        iso = d.isoformat()
        if d.weekday() < 5 and iso not in feriados_set:  # 0=Seg ... 4=Sex
            dias.append(iso)
        d += timedelta(days=1)
    return dias


def data_br_para_iso(data_br):
    # "24/07/2026" -> "2026-07-24"
    dia, mes, ano = data_br.split("/")
    return f"{ano}-{mes}-{dia}"


def classifica_dia(dia_registro, dias_uteis_set):
    """Retorna (tipo, motivo) onde tipo in {None, 'cheia', 'meia'}. None = não conta (fim de semana/feriado)."""
    data_iso = data_br_para_iso(dia_registro["data"])
    if data_iso not in dias_uteis_set:
        return None, None  # fim de semana ou feriado — nunca conta, mesmo que o motivo diga outra coisa

    hn_min = parse_hhmm_to_minutes(dia_registro.get("horas_normais"))
    motivo = (dia_registro.get("motivo") or "").strip()

    if hn_min is None or hn_min == 0:
        return "cheia", motivo or "(sem motivo registrado no ponto)"
    if hn_min < 6 * 60:
        return "meia", motivo or "(sem motivo registrado no ponto)"
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ponto_json")
    ap.add_argument("--mes", type=int, required=True)
    ap.add_argument("--ano", type=int, required=True)
    ap.add_argument("--feriados", default=None, help="Caminho do references/feriados_belem.json")
    ap.add_argument("--horas-dia", type=float, default=8.8)
    ap.add_argument("--qtd-funcionarios", type=int, default=27)
    ap.add_argument("--incluir-pontos-facultativos", action="store_true")
    ap.add_argument("--employee-list", default=None,
                     help="JSON com lista de nomes esperados (['NOME1','NOME2',...]) pra conferência")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    script_dir = Path(__file__).parent
    feriados_path = args.feriados or (script_dir.parent / "references" / "feriados_belem.json")
    feriados_set, feriados_origem = carrega_feriados(feriados_path, args.ano, args.incluir_pontos_facultativos)

    dias_uteis = dias_uteis_do_mes(args.mes, args.ano, feriados_set)
    n_dias_uteis = len(dias_uteis)
    dias_uteis_set = set(dias_uteis)

    ponto = json.loads(Path(args.ponto_json).read_text(encoding="utf-8"))

    resultado_funcionarios = []
    total_faltas_geral = 0.0

    for f in ponto["funcionarios"]:
        faltas_lista = []
        total_faltas_func = 0.0
        for dia in f["dias"]:
            tipo, motivo = classifica_dia(dia, dias_uteis_set)
            if tipo == "cheia":
                total_faltas_func += 1.0
                faltas_lista.append({"data": dia["data"], "dia_semana": dia["dia_semana"],
                                      "tipo": "falta cheia (1,0)", "motivo": motivo})
            elif tipo == "meia":
                total_faltas_func += 0.5
                faltas_lista.append({"data": dia["data"], "dia_semana": dia["dia_semana"],
                                      "tipo": "meia falta (0,5)", "motivo": motivo})
        resultado_funcionarios.append({
            "colaborador": f["colaborador"],
            "dias_registrados_no_ponto": len(f["dias"]),
            "total_faltas": round(total_faltas_func, 1),
            "faltas": faltas_lista,
        })
        total_faltas_geral += total_faltas_func

    # checagem contra lista de funcionários esperada, se fornecida
    checagem_lista = None
    if args.employee_list:
        esperados = set(json.loads(Path(args.employee_list).read_text(encoding="utf-8")))
        encontrados = {f["colaborador"] for f in ponto["funcionarios"]}
        checagem_lista = {
            "esperados_nao_encontrados_no_ponto": sorted(esperados - encontrados),
            "encontrados_no_ponto_nao_esperados": sorted(encontrados - esperados),
        }

    horas_dia = args.horas_dia
    qtd_func = args.qtd_funcionarios
    hpr = round(horas_dia * qtd_func * n_dias_uteis, 2)
    ht = round(hpr - (total_faltas_geral * horas_dia), 2)
    dsc = round((ht / hpr) * 100, 2) if hpr else None

    saida = {
        "periodo": f"{args.mes:02d}/{args.ano}",
        "dias_uteis_no_mes": n_dias_uteis,
        "dias_uteis_lista": dias_uteis,
        "feriados_excluidos_no_mes": {d: n for d, n in feriados_origem.items() if d.startswith(f"{args.ano}-{args.mes:02d}")},
        "parametros_indicador": {"horas_trabalho_dia": horas_dia, "quantidade_funcionarios": qtd_func},
        "total_faltas_sugerido_dias": round(total_faltas_geral, 1),
        "indicador_3_dsc_sugerido": {
            "HPR_horas_totais_previstas": hpr,
            "HT_horas_efetivamente_trabalhadas": ht,
            "DSC_percentual": dsc,
            "observacao": "Este 'total_faltas_sugerido' e o DSC daqui são um PONTO DE PARTIDA. "
                           "Revise a lista de faltas abaixo, ajuste manualmente o total de faltas "
                           "considerado válido, e recalcule HT/DSC com o número final."
        },
        "checagem_lista_funcionarios": checagem_lista,
        "funcionarios": resultado_funcionarios,
    }

    out_path = Path(args.out) if args.out else Path(args.ponto_json).with_name("indicador3.json")
    out_path.write_text(json.dumps(saida, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK -> {out_path}", file=sys.stderr)
    print(f"Dias úteis: {n_dias_uteis} | Total faltas sugerido: {total_faltas_geral} | DSC sugerido: {dsc}%", file=sys.stderr)


if __name__ == "__main__":
    main()
