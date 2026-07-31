"""Camada de acesso ao banco de dados (SQLite em arquivo único).

Decisões importantes para funcionar bem em pasta de rede compartilhada,
com múltiplos computadores acessando o mesmo arquivo (uso revezado, não
simultâneo pesado):

- journal_mode = DELETE (não WAL). O modo WAL depende de memória
  compartilhada (mmap) que costuma falhar ou se corromper em
  compartilhamentos de rede (SMB/CIFS). O modo DELETE é o tradicional do
  SQLite e é seguro em rede.
- synchronous = FULL, para reduzir o risco de corrupção em caso de queda de
  energia/rede no meio de uma gravação.
- busy_timeout alto, para que, se dois computadores tentarem gravar quase
  ao mesmo tempo, o segundo espere alguns segundos em vez de falhar na hora.
- Conexões de curta duração: cada operação abre e fecha sua própria conexão,
  em vez de manter uma conexão aberta o tempo todo. Isso evita segurar
  bloqueios/handles de arquivo de rede por longos períodos.
- Erros de bloqueio (`database is locked`) e de indisponibilidade da pasta
  de rede são convertidos em exceções amigáveis, tratadas na interface.
"""
from __future__ import annotations

import sqlite3
import time
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional

BUSY_TIMEOUT_MS = 8000
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 1.5

CATEGORIAS_PADRAO = [
    "Fluxômetro",
    "Manômetro",
    "Regulador de Cilindro",
    "Válvula",
    "Cilindro",
    "Umidificador",
    "Outro",
]

TIPOS_MOVIMENTACAO = ("ENTRADA", "SAIDA")


class BancoIndisponivelError(Exception):
    """A pasta/arquivo do banco de dados não pôde ser acessado."""


class BancoBloqueadoError(Exception):
    """O arquivo do banco está sendo usado por outro computador no momento."""


@dataclass
class Item:
    id: int
    nome: str
    categoria: str
    unidade_medida: str
    estoque_minimo: float
    ativo: bool


@dataclass
class Movimentacao:
    id: int
    tipo: str
    item_id: int
    item_nome: str
    quantidade: float
    solicitante: str
    setor: str
    numero_serie: str
    responsavel_registro: str
    data_hora: str
    observacao: str


def _translate_error(exc: sqlite3.OperationalError, db_path: Path) -> Exception:
    msg = str(exc).lower()
    if "locked" in msg or "busy" in msg:
        return BancoBloqueadoError(
            "O arquivo de banco de dados está sendo usado por outro "
            "computador neste momento. Aguarde alguns segundos e tente "
            "novamente."
        )
    if "unable to open database file" in msg or "disk i/o error" in msg or "no such file or directory" in msg:
        return BancoIndisponivelError(
            f"Não foi possível acessar o banco de dados em:\n{db_path}\n\n"
            "Verifique se a pasta compartilhada de rede está disponível "
            "(computador ligado, cabo de rede conectado, unidade mapeada) "
            "e tente novamente. Você também pode ajustar o caminho em "
            "Configurações."
        )
    return exc


@contextmanager
def get_connection(db_path: Path):
    db_path = Path(db_path)
    try:
        db_path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise BancoIndisponivelError(
            f"Não foi possível acessar a pasta do banco de dados:\n{db_path.parent}\n\n"
            f"Detalhe: {exc}"
        ) from exc

    last_exc: Optional[Exception] = None
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect(str(db_path), timeout=BUSY_TIMEOUT_MS / 1000)
            conn.execute(f"PRAGMA busy_timeout = {BUSY_TIMEOUT_MS}")
            conn.execute("PRAGMA journal_mode = DELETE")
            conn.execute("PRAGMA synchronous = FULL")
            conn.execute("PRAGMA foreign_keys = ON")
            conn.row_factory = sqlite3.Row
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                conn.close()
            return
        except sqlite3.OperationalError as exc:
            last_exc = _translate_error(exc, db_path)
            if isinstance(last_exc, BancoBloqueadoError) and attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BACKOFF_SECONDS)
                continue
            raise last_exc
    if last_exc:
        raise last_exc


SCHEMA = """
CREATE TABLE IF NOT EXISTS itens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    unidade_medida TEXT NOT NULL,
    estoque_minimo REAL NOT NULL DEFAULT 0,
    ativo INTEGER NOT NULL DEFAULT 1,
    criado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS movimentacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL CHECK (tipo IN ('ENTRADA', 'SAIDA')),
    item_id INTEGER NOT NULL REFERENCES itens(id),
    quantidade REAL NOT NULL CHECK (quantidade > 0),
    solicitante TEXT NOT NULL,
    setor TEXT NOT NULL DEFAULT '',
    numero_serie TEXT NOT NULL DEFAULT '',
    responsavel_registro TEXT NOT NULL,
    data_hora TEXT NOT NULL,
    observacao TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_mov_item ON movimentacoes(item_id);
CREATE INDEX IF NOT EXISTS idx_mov_data ON movimentacoes(data_hora);
"""


def init_db(db_path: Path) -> None:
    with get_connection(db_path) as conn:
        conn.executescript(SCHEMA)


# ---------------------------------------------------------------------------
# Itens
# ---------------------------------------------------------------------------

def list_itens(db_path: Path, somente_ativos: bool = False) -> list[Item]:
    query = "SELECT id, nome, categoria, unidade_medida, estoque_minimo, ativo FROM itens"
    if somente_ativos:
        query += " WHERE ativo = 1"
    query += " ORDER BY nome COLLATE NOCASE"
    with get_connection(db_path) as conn:
        rows = conn.execute(query).fetchall()
    return [
        Item(row["id"], row["nome"], row["categoria"], row["unidade_medida"],
             row["estoque_minimo"], bool(row["ativo"]))
        for row in rows
    ]


def add_item(db_path: Path, nome: str, categoria: str, unidade_medida: str,
             estoque_minimo: float) -> int:
    with get_connection(db_path) as conn:
        cur = conn.execute(
            "INSERT INTO itens (nome, categoria, unidade_medida, estoque_minimo, ativo, criado_em) "
            "VALUES (?, ?, ?, ?, 1, ?)",
            (nome.strip(), categoria.strip(), unidade_medida.strip(), estoque_minimo,
             datetime.now().isoformat(timespec="seconds")),
        )
        return cur.lastrowid


def update_item(db_path: Path, item_id: int, nome: str, categoria: str,
                 unidade_medida: str, estoque_minimo: float) -> None:
    with get_connection(db_path) as conn:
        conn.execute(
            "UPDATE itens SET nome = ?, categoria = ?, unidade_medida = ?, estoque_minimo = ? "
            "WHERE id = ?",
            (nome.strip(), categoria.strip(), unidade_medida.strip(), estoque_minimo, item_id),
        )


def set_item_ativo(db_path: Path, item_id: int, ativo: bool) -> None:
    with get_connection(db_path) as conn:
        conn.execute("UPDATE itens SET ativo = ? WHERE id = ?", (1 if ativo else 0, item_id))


# ---------------------------------------------------------------------------
# Movimentações
# ---------------------------------------------------------------------------

def add_movimentacao(db_path: Path, tipo: str, item_id: int, quantidade: float,
                      solicitante: str, setor: str, numero_serie: str,
                      responsavel_registro: str, observacao: str) -> int:
    if tipo not in TIPOS_MOVIMENTACAO:
        raise ValueError(f"Tipo de movimentação inválido: {tipo}")
    with get_connection(db_path) as conn:
        cur = conn.execute(
            "INSERT INTO movimentacoes "
            "(tipo, item_id, quantidade, solicitante, setor, numero_serie, "
            " responsavel_registro, data_hora, observacao) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (tipo, item_id, quantidade, solicitante.strip(), setor.strip(),
             numero_serie.strip(), responsavel_registro.strip(),
             datetime.now().isoformat(timespec="seconds"), observacao.strip()),
        )
        return cur.lastrowid


def estoque_atual(db_path: Path) -> dict[int, float]:
    """Retorna {item_id: saldo_atual} calculado a partir do histórico."""
    query = """
        SELECT i.id AS item_id,
               COALESCE(SUM(CASE WHEN m.tipo = 'ENTRADA' THEN m.quantidade
                                  WHEN m.tipo = 'SAIDA' THEN -m.quantidade
                                  ELSE 0 END), 0) AS saldo
        FROM itens i
        LEFT JOIN movimentacoes m ON m.item_id = i.id
        GROUP BY i.id
    """
    with get_connection(db_path) as conn:
        rows = conn.execute(query).fetchall()
    return {row["item_id"]: row["saldo"] for row in rows}


def list_movimentacoes(db_path: Path, item_id: Optional[int] = None,
                        tipo: Optional[str] = None,
                        data_inicio: Optional[str] = None,
                        data_fim: Optional[str] = None,
                        solicitante: Optional[str] = None) -> list[Movimentacao]:
    query = """
        SELECT m.id, m.tipo, m.item_id, i.nome AS item_nome, m.quantidade,
               m.solicitante, m.setor, m.numero_serie, m.responsavel_registro,
               m.data_hora, m.observacao
        FROM movimentacoes m
        JOIN itens i ON i.id = m.item_id
        WHERE 1 = 1
    """
    params: list = []
    if item_id:
        query += " AND m.item_id = ?"
        params.append(item_id)
    if tipo:
        query += " AND m.tipo = ?"
        params.append(tipo)
    if data_inicio:
        query += " AND m.data_hora >= ?"
        params.append(data_inicio)
    if data_fim:
        query += " AND m.data_hora <= ?"
        params.append(data_fim)
    if solicitante:
        query += " AND m.solicitante LIKE ?"
        params.append(f"%{solicitante}%")
    query += " ORDER BY m.data_hora DESC, m.id DESC"

    with get_connection(db_path) as conn:
        rows = conn.execute(query, params).fetchall()
    return [
        Movimentacao(row["id"], row["tipo"], row["item_id"], row["item_nome"],
                     row["quantidade"], row["solicitante"], row["setor"],
                     row["numero_serie"], row["responsavel_registro"],
                     row["data_hora"], row["observacao"])
        for row in rows
    ]


def list_distinct_values(db_path: Path, coluna: str) -> list[str]:
    assert coluna in ("solicitante", "responsavel_registro", "setor")
    with get_connection(db_path) as conn:
        rows = conn.execute(
            f"SELECT DISTINCT {coluna} FROM movimentacoes "
            f"WHERE {coluna} != '' ORDER BY {coluna} COLLATE NOCASE"
        ).fetchall()
    return [row[0] for row in rows]
