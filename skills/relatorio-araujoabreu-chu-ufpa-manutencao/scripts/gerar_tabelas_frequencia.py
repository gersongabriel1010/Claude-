#!/usr/bin/env python3
"""
Gera as duas tabelas da análise de frequência, em texto separado por TAB (pronto pra copiar do
chat e colar direto no Excel, na célula A1):

  1) ANÁLISE DA FREQUÊNCIA — todos os funcionários da relação, ordem alfabética:
       Nome | Função | Observação | SUBSTITUTO
  2) RELATÓRIO DE FALTAS MÊS <MÊS> — quem teve falta, quem não consta no ponto, quem cobre
     faltas, postos do Termo Aditivo e desligados; ordem decrescente de faltas:
       Funcionário | Função | Faltas | Detalhe
     seguido do subtotal de faltas por função e do TOTAL.

Entrada: o indicador3.json gerado por calc_indicador3.py COM --relacao (só funcionários da
relação). Os números são a SUGESTÃO da regra do ponto — o fiscal revisa antes de usar.

Uso:
    python3 gerar_tabelas_frequencia.py indicador3.json [--out-dir saida/]
Imprime as duas tabelas no stdout (separadas por uma linha em branco) e, com --out-dir, grava
analise_frequencia.tsv e relatorio_faltas.tsv.
"""
import argparse
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

MESES = ["", "JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO",
         "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]

# palavra-chave no motivo do ponto -> rótulo usado nas tabelas (ordem = prioridade)
MOTIVOS = [
    ("FERIAS", "férias"),
    ("ATESTADO", "atestado médico"),
    ("DOACAO DE SANGUE", "doação de sangue"),
    ("LIBERACAO DO CLIENTE", "liberação do cliente"),
    ("LIBERACAO DO GERENTE", "liberação do gerente"),
    ("DECLARACAO DE COMPARECIMENTO", "declaração de comparecimento"),
    ("LICENCA", "licença"),
    ("ADESAO", "abono Adesão do Pará"),
]

PLURAIS = {"Mecânico": "mecânicos", "Ajudante": "ajudantes", "Auxiliar": "auxiliares",
           "Técnico": "técnicos", "Oficial": "oficiais"}


def sem_acento(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().upper()


def num(v, casas=None):
    """1.0 -> '1', 0.5 -> '0,5'; com casas=2 -> '1,00'."""
    if casas is not None:
        return f"{v:.{casas}f}".replace(".", ",")
    return (f"{v:.1f}".rstrip("0").rstrip(".")).replace(".", ",")


def data_br(iso):
    return f"{iso[8:10]}/{iso[5:7]}/{iso[0:4]}" if iso else ""


def lista_pt(itens):
    return itens[0] if len(itens) == 1 else ", ".join(itens[:-1]) + " e " + itens[-1]


POS_DESLIG = "sem substituto após desligamento"


def rotulo_motivo(falta):
    if falta.get("pos_desligamento"):
        return POS_DESLIG
    if falta.get("ausente_da_folha"):
        return "dia ausente da folha de ponto (verificar)"
    m = falta["motivo"]
    if m == "(sem motivo registrado no ponto)":
        if falta.get("sem_marcacao"):
            return "sem registro de ponto e sem motivo"
        return "sem motivo, com marcação de ponto (verificar)"
    mn = sem_acento(m)
    for chave, rotulo in MOTIVOS:
        if chave in mn:
            return rotulo
    return m.split(" | ")[0].strip().lower()


def compensacao(falta, ano):
    """Folga por liberação do cliente: acha no texto do motivo o sábado/domingo trabalhado."""
    if "LIBERACAO DO CLIENTE" not in sem_acento(falta["motivo"]):
        return None
    dia_falta = falta["data"][:5]
    for d, m in re.findall(r"(\d{1,2})\s*/\s*(\d{1,2})", falta["motivo"]):
        dd = f"{int(d):02d}/{int(m):02d}"
        if dd == dia_falta:
            continue
        try:
            wd = date(ano, int(m), int(d)).weekday()
        except ValueError:
            continue
        if wd in (5, 6):
            return f"folga pelo {'sábado' if wd == 5 else 'domingo'} {dd}"
    return None


def agrupa(faltas, dias_uteis, ano):
    """Agrupa faltas por (motivo, compensação, meia) e formata datas, juntando sequências de
    3+ dias úteis seguidos em 'dd/mm a dd/mm'. Retorna lista de (rotulo, extra, texto_datas, meia)."""
    pos = {data_br(d)[:5]: i for i, d in enumerate(dias_uteis)}
    grupos = {}
    for f in faltas:
        meia = f["valor"] == 0.5
        chave = (rotulo_motivo(f), compensacao(f, ano), meia)
        grupos.setdefault(chave, []).append(f["data"][:5])
    saida = []
    for (rotulo, extra, meia), datas in grupos.items():
        if meia:
            texto = lista_pt([f"{d} (0,5)" for d in datas])
        else:
            blocos, atual = [], [datas[0]]
            for d in datas[1:]:
                if d in pos and atual[-1] in pos and pos[d] == pos[atual[-1]] + 1:
                    atual.append(d)
                else:
                    blocos.append(atual)
                    atual = [d]
            blocos.append(atual)
            partes = []
            for b in blocos:
                partes.extend([f"{b[0]} a {b[-1]}"] if len(b) >= 3 else b)
            texto = lista_pt(partes)
        if rotulo == POS_DESLIG:
            extra = f"{len(datas)} {'dia' if len(datas) == 1 else 'dias'}"
        saida.append((rotulo, extra, texto, meia))
    return saida


def faixa_br(isos):
    if len(isos) == 1:
        return data_br(isos[0])[:5]
    return f"{data_br(isos[0])[:5]} a {data_br(isos[-1])[:5]}"


def texto_faltas(total):
    return f"{num(total)} {'falta' if total <= 1 else 'faltas'}"


def montar(ind3):
    mes, ano = ind3["mes"], ind3["ano"]
    nome_mes = MESES[mes]
    ini_mes, fim_mes = f"{ano}-{mes:02d}-01", f"{ano}-{mes:02d}-31"
    dias_uteis = ind3["dias_uteis_lista"]

    linhas_analise, linhas_faltas = [], []
    for f in ind3["funcionarios"]:
        total = f["total_faltas"]
        grupos = agrupa(f["faltas"], dias_uteis, ano) if f["faltas"] else []
        admitido_no_mes = f.get("admissao") and f["admissao"] >= ini_mes
        desligado = f.get("demissao") and f["demissao"] <= fim_mes

        # ---------- Tabela 1: Observação ----------
        obs = []
        if f.get("registrado_como"):
            obs.append(f"Posto via Termo Aditivo — ponto registrado sob o nome '{f['registrado_como']}'")
        elif f.get("aditivo"):
            obs.append("Posto incluído via Termo Aditivo")
        if f.get("cobre_faltas"):
            plural = PLURAIS.get(f["funcao"].split()[0], "colaboradores")
            obs.append(f"Função: cobrir faltas de outros {plural}")
        antes_adm = f.get("dias_antes_admissao") or []
        if admitido_no_mes:
            obs.append(f"Admitido em {data_br(f['admissao'])}" + (
                f"; {faixa_br(antes_adm)} antes da admissão – não contados" if antes_adm
                else " (ponto só a partir dessa data)"))
        if desligado:
            obs.append(f"Desligado em {data_br(f['demissao'])}")
        if not f["consta_no_ponto"]:
            obs.append(f"Não consta na folha de ponto de {nome_mes.lower()} – verificar situação")
        elif grupos:
            if len(grupos) == 1:
                rot, extra, datas, meia = grupos[0]
                if meia:  # o total "0,5 falta" já diz que é meia; evita "(22/09 (0,5))"
                    datas = datas.replace(" (0,5)", "")
                det = f"{rot} – {datas}" + (f", {extra}" if extra else "")
            else:
                det = "; ".join(f"{datas} {rot}" + (f" ({extra})" if extra else "")
                                for rot, extra, datas, _ in grupos)
            obs.append(f"{texto_faltas(total)} ({det})")
        elif obs and not f.get("alertas"):
            obs.append("sem intercorrências")
        if f.get("alertas"):
            obs.append("conferir: divergência entre relação e ponto (ver pendências)")
        observacao = "; ".join(obs) if obs else "Sem intercorrências"
        nome = f["colaborador"] + (f" ({f['registrado_como']})" if f.get("registrado_como") else "")
        linhas_analise.append((nome, f["funcao"], observacao))

        # ---------- Tabela 2: Relatório de faltas ----------
        entra = (not f["consta_no_ponto"]) or (total or 0) > 0 or f.get("aditivo") \
            or f.get("cobre_faltas") or desligado or antes_adm or f.get("alertas")
        if entra:
            det = []
            if f.get("cobre_faltas"):
                det.append("cobrindo faltas")
            if desligado:
                det.append(f"desligado em {data_br(f['demissao'])}")
            if admitido_no_mes:
                det.append(f"admitido em {data_br(f['admissao'])}" + (
                    f"; {faixa_br(antes_adm)} antes da admissão – não contados" if antes_adm else ""))
            if not f["consta_no_ponto"]:
                det.append(f"não consta na folha de ponto de {nome_mes.lower()} – verificar")
            det.extend(f"{datas} {rot}" + (f" ({extra})" if extra else "") for rot, extra, datas, _ in grupos)
            if f.get("alertas"):
                det.append("conferir: divergência entre relação e ponto")
            linhas_faltas.append((nome, f["funcao"], total, "; ".join(det)))

    linhas_analise.sort(key=lambda l: sem_acento(l[0]))
    linhas_faltas.sort(key=lambda l: (-(l[2] or 0), 0 if l[2] is None else 1, sem_acento(l[0])))

    t1 = ["ANÁLISE DA FREQUÊNCIA\t\t\t", "Nome\tFunção\tObservação\tSUBSTITUTO"]
    t1 += [f"{n}\t{fn}\t{o}\t" for n, fn, o in linhas_analise]

    t2 = [f"RELATÓRIO DE FALTAS MÊS {nome_mes}\t\t\t", "Funcionário\tFunção\tFaltas\tDetalhe"]
    t2 += [f"{n}\t{fn}\t{'' if t is None else num(t, 2)}\t{d}" for n, fn, t, d in linhas_faltas]

    por_funcao = {}
    for f in ind3["funcionarios"]:
        por_funcao[f["funcao"]] = por_funcao.get(f["funcao"], 0) + (f["total_faltas"] or 0)
    t2.append("\t\t\t")
    for fn in sorted(por_funcao, key=sem_acento):
        t2.append(f"SUBTOTAL\t{fn}\t{num(por_funcao[fn], 2)}\t")
    total_geral = sum(por_funcao.values())
    t2.append(f"TOTAL\t\t{num(total_geral, 2)}\t")
    return "\n".join(t1), "\n".join(t2), total_geral


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("indicador3_json")
    ap.add_argument("--out-dir", default=None)
    args = ap.parse_args()

    ind3 = json.loads(Path(args.indicador3_json).read_text(encoding="utf-8"))
    if not ind3.get("filtrado_pela_relacao"):
        sys.exit("ERRO: rode calc_indicador3.py com --relacao <planilha da relação de funcionários>; "
                 "as tabelas só podem conter quem está na relação.")

    analise, faltas, total = montar(ind3)
    print(analise)
    print()
    print(faltas)

    if args.out_dir:
        out = Path(args.out_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "analise_frequencia.tsv").write_text(analise + "\n", encoding="utf-8")
        (out / "relatorio_faltas.tsv").write_text(faltas + "\n", encoding="utf-8")

    chk = ind3.get("checagem_lista_funcionarios") or {}
    print(f"\nTotal de faltas (só relação): {num(total, 2)}", file=sys.stderr)
    if chk.get("pendencias_datas"):
        print("Pendências (relação x ponto) — confirmar com o usuário:", file=sys.stderr)
        for pend in chk["pendencias_datas"]:
            print(f"  - {pend}", file=sys.stderr)
    if chk.get("na_relacao_sem_ponto"):
        print("Na relação mas sem ponto: " + ", ".join(chk["na_relacao_sem_ponto"]), file=sys.stderr)
    if ind3.get("fora_da_relacao"):
        print("No ponto mas fora da relação (não entram): " + ", ".join(
            f"{f['colaborador']} ({num(f['total_faltas_no_ponto'])})" for f in ind3["fora_da_relacao"]),
            file=sys.stderr)


if __name__ == "__main__":
    main()
