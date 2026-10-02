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

Com --relacao (planilha "Relação de Funcionários" do mês), só os funcionários da relação entram
no total/DSC; quem está no ponto mas fora da relação vai pra `fora_da_relacao` (só informativo).
Dias anteriores à admissão não contam; dias posteriores ao desligamento contam e são marcados
como "pós-desligamento" (vaga sem substituto).

O total de faltas calculado aqui é uma SUGESTÃO para revisão manual — o fiscal decide o
número final que entra na fórmula do indicador (ver campo "faltas_sugeridas" vs. o que for
efetivamente usado).

Uso:
    python3 calc_indicador3.py <ponto_extraido.json> --mes 7 --ano 2026 \
        [--feriados feriados_belem.json] [--horas-dia 8.8] [--qtd-funcionarios 27] \
        [--relacao relacao_funcionarios.xlsx] [--out indicador3.json]
"""
import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

from relacao import carrega_relacao, casa_relacao_com_ponto

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


def tem_marcacao(dia):
    return any(dia.get(k) for k in ("1a_entrada", "1a_saida", "2a_entrada", "2a_saida"))


def iso_para_br(iso):
    return f"{iso[8:10]}/{iso[5:7]}"


def faixa(isos):
    return iso_para_br(isos[0]) if len(isos) == 1 else f"{iso_para_br(isos[0])} a {iso_para_br(isos[-1])}"


def apura_funcionario(dias, dias_uteis, admissao=None, demissao=None):
    """Faltas de um funcionário no mês + conferência das datas da relação contra o ponto.

    Nada é descartado em silêncio:
      - dias úteis antes da admissão não contam, mas voltam em `dias_antes_admissao`;
      - dia útil que nem aparece na folha de ponto conta como falta ("dia ausente da folha");
      - dias depois do desligamento contam (marcados `pos_desligamento`);
      - divergências entre as datas da relação e o ponto voltam em `alertas`.
    """
    adm = admissao.isoformat() if admissao else None
    dem = demissao.isoformat() if demissao else None
    por_data = {data_br_para_iso(d["data"]): d for d in dias}
    uteis_set = set(dias_uteis)
    faltas, total, antes_adm, alertas = [], 0.0, [], []

    for d_iso in dias_uteis:
        dia = por_data.get(d_iso)
        if adm and d_iso < adm:
            antes_adm.append(d_iso)
            continue
        pos = bool(dem and d_iso > dem)
        if dia is None:
            tipo, motivo, sem_marc = "cheia", "dia ausente da folha de ponto", True
        else:
            tipo, motivo = classifica_dia(dia, uteis_set)
            sem_marc = not tem_marcacao(dia)
            if tipo is None:
                continue
        if pos and motivo == "(sem motivo registrado no ponto)":
            motivo = "sem motivo (pós-desligamento)"
        valor = 1.0 if tipo == "cheia" else 0.5
        total += valor
        faltas.append({"data": f"{d_iso[8:10]}/{d_iso[5:7]}/{d_iso[0:4]}",
                       "dia_semana": dia["dia_semana"] if dia else "",
                       "tipo": "falta cheia (1,0)" if tipo == "cheia" else "meia falta (0,5)",
                       "valor": valor, "motivo": motivo, "sem_marcacao": sem_marc,
                       "pos_desligamento": pos, "ausente_da_folha": dia is None})

    # --- conferência das datas da relação contra o ponto ---
    ausentes = [data_br_para_iso(f["data"]) for f in faltas if f["ausente_da_folha"] and not f["pos_desligamento"]]
    if ausentes:
        alertas.append(f"{len(ausentes)} dia(s) útil(eis) não aparecem na folha de ponto "
                       f"({', '.join(iso_para_br(x) for x in ausentes)}) — contados como falta; conferir")
    if adm:
        marc_antes = sorted(x for x, d in por_data.items() if x < adm and tem_marcacao(d))
        if marc_antes:
            alertas.append(f"há marcação de ponto antes da admissão informada na relação "
                           f"({data_br(adm)}): {', '.join(iso_para_br(x) for x in marc_antes)} — "
                           f"data de admissão provavelmente errada")
        if antes_adm and not marc_antes:
            alertas.append(f"{len(antes_adm)} dia(s) útil(eis) antes da admissão ({data_br(adm)}) "
                           f"não contados: {faixa(antes_adm)} — confirmar a data de admissão")
        if adm >= dias_uteis[0]:
            vazios = []
            for x in (u for u in dias_uteis if u >= adm):
                if por_data.get(x) and tem_marcacao(por_data[x]):
                    break
                vazios.append(x)
            if vazios and len(vazios) < len([u for u in dias_uteis if u >= adm]):
                alertas.append(f"sem marcação de {faixa(vazios)}, logo após a admissão ({data_br(adm)}) — "
                               f"contados como falta; confirmar a data de admissão")
    if dem:
        marc_depois = sorted(x for x, d in por_data.items() if x > dem and tem_marcacao(d))
        if marc_depois:
            alertas.append(f"há marcação de ponto depois do desligamento informado na relação "
                           f"({data_br(dem)}): {', '.join(iso_para_br(x) for x in marc_depois)} — "
                           f"data de desligamento provavelmente errada")
    else:
        cauda = []
        for x in reversed(dias_uteis):
            d = por_data.get(x)
            if d is None or (not tem_marcacao(d) and not (d.get("motivo") or "").strip()):
                cauda.insert(0, x)
            else:
                break
        if len(cauda) >= 3:
            alertas.append(f"sem marcação e sem motivo de {faixa(cauda)} (até o fim do mês) e sem data de "
                           f"demissão na relação — possível desligamento não informado")
    return {"total": round(total, 1), "faltas": faltas, "dias_antes_admissao": antes_adm, "alertas": alertas}


def data_br(iso):
    return f"{iso[8:10]}/{iso[5:7]}/{iso[0:4]}"


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
    ap.add_argument("--relacao", default=None,
                     help="Planilha (.xlsx/.csv) com a Relação de Funcionários do mês. Recomendado: "
                          "só quem está nela entra no total de faltas/DSC.")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    script_dir = Path(__file__).parent
    feriados_path = args.feriados or (script_dir.parent / "references" / "feriados_belem.json")
    feriados_set, feriados_origem = carrega_feriados(feriados_path, args.ano, args.incluir_pontos_facultativos)

    dias_uteis = dias_uteis_do_mes(args.mes, args.ano, feriados_set)
    n_dias_uteis = len(dias_uteis)
    dias_uteis_set = set(dias_uteis)

    ponto = json.loads(Path(args.ponto_json).read_text(encoding="utf-8"))

    registros_ponto = {f["colaborador"]: f for f in ponto["funcionarios"]}

    def apura(dias, admissao=None, demissao=None):
        r = apura_funcionario(dias, dias_uteis, admissao, demissao)
        return r["total"], r["faltas"], r["dias_antes_admissao"], r["alertas"]

    resultado_funcionarios = []
    fora_da_relacao = None
    checagem_lista = None

    if args.relacao:
        relacao, nomes_fora = casa_relacao_com_ponto(carrega_relacao(args.relacao), list(registros_ponto))
        for f in relacao:
            reg = registros_ponto.get(f["nome_no_ponto"])
            total_f, faltas_f, antes_adm, alertas_f = (apura(reg["dias"], f["admissao"], f["demissao"])
                                                       if reg else (None, [], [], []))
            resultado_funcionarios.append({
                "colaborador": f["nome"],
                "nome_no_ponto": f["nome_no_ponto"],
                "consta_no_ponto": reg is not None,
                "funcao": f["funcao"],
                "observacao_relacao": f["observacao"],
                "aditivo": f["aditivo"],
                "cobre_faltas": f["cobre_faltas"],
                "registrado_como": f["registrado_como"],
                "admissao": f["admissao"].isoformat() if f["admissao"] else None,
                "demissao": f["demissao"].isoformat() if f["demissao"] else None,
                "dias_registrados_no_ponto": len(reg["dias"]) if reg else 0,
                "total_faltas": total_f,
                "faltas": faltas_f,
                "dias_antes_admissao": antes_adm,
                "alertas": alertas_f,
            })
        fora_da_relacao = []
        for n in nomes_fora:
            total_f, *_ = apura(registros_ponto[n]["dias"])
            fora_da_relacao.append({"colaborador": n, "total_faltas_no_ponto": total_f})
        pendencias = [f"{f['colaborador']}: {a}" for f in resultado_funcionarios for a in f["alertas"]]
        checagem_lista = {
            "pendencias_datas": pendencias,
            "na_relacao_sem_ponto": [f["colaborador"] for f in resultado_funcionarios if not f["consta_no_ponto"]],
            "no_ponto_fora_da_relacao": nomes_fora,
        }
    else:
        for f in ponto["funcionarios"]:
            total_f, faltas_f, _, _ = apura(f["dias"])
            resultado_funcionarios.append({
                "colaborador": f["colaborador"],
                "dias_registrados_no_ponto": len(f["dias"]),
                "total_faltas": total_f,
                "faltas": faltas_f,
            })
        if args.employee_list:
            esperados = set(json.loads(Path(args.employee_list).read_text(encoding="utf-8")))
            encontrados = set(registros_ponto)
            checagem_lista = {
                "esperados_nao_encontrados_no_ponto": sorted(esperados - encontrados),
                "encontrados_no_ponto_nao_esperados": sorted(encontrados - esperados),
            }

    total_faltas_geral = sum(f["total_faltas"] or 0 for f in resultado_funcionarios)

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
        "mes": args.mes,
        "ano": args.ano,
        "filtrado_pela_relacao": bool(args.relacao),
        "checagem_lista_funcionarios": checagem_lista,
        "fora_da_relacao": fora_da_relacao,
        "funcionarios": resultado_funcionarios,
    }

    out_path = Path(args.out) if args.out else Path(args.ponto_json).with_name("indicador3.json")
    out_path.write_text(json.dumps(saida, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK -> {out_path}", file=sys.stderr)
    print(f"Dias úteis: {n_dias_uteis} | Total faltas sugerido: {total_faltas_geral} | DSC sugerido: {dsc}%", file=sys.stderr)


if __name__ == "__main__":
    main()
