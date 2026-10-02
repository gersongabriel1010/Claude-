#!/usr/bin/env python3
"""
Leitura da "Relação de Funcionários" do mês (planilha .xlsx/.csv enviada pela contratada) e
casamento de cada nome da relação com o nome correspondente na folha de ponto (Pontomais).

Por que existe: a relação é a lista oficial de quem ocupa os postos do contrato no mês. Só quem
está nela entra no cálculo de faltas/DSC — a folha de ponto costuma trazer gente de outros
contratos ou coberturas, e somar todo mundo do ponto infla o total de faltas.

Casamento de nomes (a relação abrevia nomes do meio, ex: "EUTHYMIOS M D S PAPASPIROPOULO" x
"EUTHYMIOS MAX DA SILVA PAPASPIROPAULOS"):
  - compara sem acento/maiúsculas;
  - cada palavra da relação precisa casar, NA ORDEM, com uma palavra do ponto: igual, inicial
    (letra única = primeira letra) ou muito parecida (erro de digitação);
  - a primeira e a última palavra da relação precisam casar com a primeira e a última do ponto
    (evita ligar "GABRIEL DA SILVA BRITO" a "KALEBE SILVA PINTO");
  - se sobrar mais de um candidato, não casa (melhor sinalizar do que errar).

Coluna OBSERVAÇÃO da relação:
  - contém "aditivo" -> posto incluído via Termo Aditivo;
  - "aditivo (Fulano)" ou "(Fulano)" -> o ponto desse posto está registrado sob o nome "Fulano";
  - contém "cobrir falta" -> função de cobrir faltas de outros colaboradores.
"""
import re
import unicodedata
from datetime import date, datetime
from difflib import SequenceMatcher
from pathlib import Path

FUNCOES_CONHECIDAS = {
    "AJUDANTE REFRIGERACAO": "Ajudante de Refrigeração",
    "AJUDANTE DE REFRIGERACAO": "Ajudante de Refrigeração",
    "AUXILIAR REFRIGERACAO": "Auxiliar de Refrigeração",
    "AUXILIAR DE REFRIGERACAO": "Auxiliar de Refrigeração",
    "MECANICO REFRIGERACAO": "Mecânico de Refrigeração",
    "MECANICO DE REFRIGERACAO": "Mecânico de Refrigeração",
    "TECNICO REFRIGERACAO": "Técnico em Refrigeração",
    "TECNICO EM REFRIGERACAO": "Técnico em Refrigeração",
    "ALMOXARIFE": "Almoxarife",
    "ENCARREGADO DE MANUTENCAO": "Encarregado de Manutenção",
    "ENCARREGADO MANUTENCAO": "Encarregado de Manutenção",
    "OFICIAL DE MANUTENCAO": "Oficial de Manutenção",
    "OFICIAL MANUTENCAO": "Oficial de Manutenção",
}

STOPWORDS = {"DE", "DA", "DO", "DAS", "DOS", "E"}


def normaliza(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", re.sub(r"[^A-Za-z ]", " ", s)).strip().upper()


def funcao_legivel(funcao_bruta):
    """'MECANICO REFRIGERACAO I' -> 'Mecânico de Refrigeração'."""
    chave = re.sub(r"\s+(I{1,3}|IV|V)$", "", normaliza(funcao_bruta))
    if chave in FUNCOES_CONHECIDAS:
        return FUNCOES_CONHECIDAS[chave]
    return " ".join(p.lower() if p in STOPWORDS else p.capitalize() for p in chave.split())


def _palavra_casa(a, b):
    if a == b:
        return True
    if len(a) == 1:
        return b.startswith(a)
    return len(a) >= 4 and len(b) >= 4 and SequenceMatcher(None, a, b).ratio() >= 0.8


def nomes_casam(nome_relacao, nome_ponto, exigir_extremos=True):
    r, p = normaliza(nome_relacao).split(), normaliza(nome_ponto).split()
    if not r or not p:
        return False
    if exigir_extremos and not (_palavra_casa(r[0], p[0]) and _palavra_casa(r[-1], p[-1])):
        return False
    i = 0
    for palavra in r:
        while i < len(p) and not _palavra_casa(palavra, p[i]):
            i += 1
        if i == len(p):
            return False
        i += 1
    return True


def acha_no_ponto(nome, nomes_ponto, exigir_extremos=True):
    """Retorna o nome do ponto que corresponde a `nome`, ou None (inclusive se ambíguo)."""
    alvo = normaliza(nome)
    exatos = [n for n in nomes_ponto if normaliza(n) == alvo]
    if len(exatos) == 1:
        return exatos[0]
    cands = [n for n in nomes_ponto if nomes_casam(nome, n, exigir_extremos)]
    return cands[0] if len(cands) == 1 else None


def _para_data(v):
    if v is None or v == "":
        return None
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", str(v).strip())
    if m:
        return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", str(v).strip())
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None


def _linhas_planilha(path):
    path = Path(path)
    if path.suffix.lower() in (".xlsx", ".xlsm"):
        import openpyxl  # pip install openpyxl
        ws = openpyxl.load_workbook(path, data_only=True).active
        return [list(r) for r in ws.iter_rows(values_only=True)]
    import csv
    texto = path.read_text(encoding="utf-8-sig")
    dialeto = csv.Sniffer().sniff(texto.splitlines()[0], delimiters=";,\t")
    return [list(r) for r in csv.reader(texto.splitlines(), dialeto)]


def _acha_coluna(cabecalho, *chaves):
    for i, c in enumerate(cabecalho):
        if any(k in normaliza(c) for k in chaves):
            return i
    return None


def carrega_relacao(path):
    """Lê a relação de funcionários. Localiza a linha de cabeçalho (a que tem 'NOME') e as
    colunas pelo título, então tolera colunas extras/fora de ordem."""
    linhas = _linhas_planilha(path)
    idx_cab = next((i for i, l in enumerate(linhas) if any("NOME" in normaliza(c) for c in l)), None)
    if idx_cab is None:
        raise ValueError(f"Não achei a linha de cabeçalho (coluna 'NOME') em {path}")
    cab = linhas[idx_cab]
    c_nome = _acha_coluna(cab, "NOME")
    c_func = _acha_coluna(cab, "FUNCAO", "CARGO")
    c_mat = _acha_coluna(cab, "MATRICULA")
    c_adm = _acha_coluna(cab, "ADMISSAO")
    c_dem = _acha_coluna(cab, "DEMISSAO", "DESLIGAMENTO")
    c_obs = _acha_coluna(cab, "OBSERVACAO", "OBS")

    def cel(l, c):
        return l[c] if c is not None and c < len(l) else None

    funcionarios = []
    for l in linhas[idx_cab + 1:]:
        nome = cel(l, c_nome)
        if not nome or not str(nome).strip():
            continue
        obs = str(cel(l, c_obs) or "").strip()
        obs_n = normaliza(obs)
        m_sub = re.search(r"\(([^)]+)\)", obs)
        funcionarios.append({
            "nome": re.sub(r"\s+", " ", str(nome)).strip(),
            "matricula": cel(l, c_mat),
            "funcao": funcao_legivel(cel(l, c_func)),
            "admissao": _para_data(cel(l, c_adm)),
            "demissao": _para_data(cel(l, c_dem)),
            "observacao": obs,
            "aditivo": "ADITIVO" in obs_n,
            "cobre_faltas": "COBRIR FALTA" in obs_n or "COBRINDO FALTA" in obs_n,
            "registrado_como": m_sub.group(1).strip() if m_sub else None,
        })
    return funcionarios


def casa_relacao_com_ponto(relacao, nomes_ponto):
    """Para cada funcionário da relação, preenche `nome_no_ponto` (ou None)."""
    for f in relacao:
        nome_ponto = None
        if f["registrado_como"]:
            # nome curto ("Mikael Mario") -> não exige casar o sobrenome final
            nome_ponto = acha_no_ponto(f["registrado_como"], nomes_ponto, exigir_extremos=False)
        if not nome_ponto:
            nome_ponto = acha_no_ponto(f["nome"], nomes_ponto)
        f["nome_no_ponto"] = nome_ponto
    usados = {f["nome_no_ponto"] for f in relacao if f["nome_no_ponto"]}
    fora_da_relacao = sorted(n for n in nomes_ponto if n not in usados)
    return relacao, fora_da_relacao
