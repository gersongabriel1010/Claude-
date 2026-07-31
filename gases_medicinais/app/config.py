"""Gerenciamento da configuração local do aplicativo.

A configuração (principalmente o caminho do arquivo de banco de dados) fica
salva em um arquivo JSON local a cada computador, dentro da pasta de dados
do usuário do sistema operacional. Isso é necessário porque o próprio
caminho do banco é configurável e pode apontar para uma pasta de rede.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

APP_FOLDER_NAME = "ControleGasesMedicinais"
CONFIG_FILE_NAME = "config.json"
DEFAULT_DB_FILE_NAME = "gases_medicinais.db"


def get_app_config_dir() -> Path:
    """Retorna a pasta onde a configuração local desta máquina fica salva.

    Windows: %APPDATA%\\ControleGasesMedicinais
    Linux/Mac (uso em desenvolvimento/testes): ~/.controle_gases_medicinais
    """
    if sys.platform.startswith("win"):
        base = os.environ.get("APPDATA")
        if not base:
            base = str(Path.home())
        return Path(base) / APP_FOLDER_NAME
    return Path.home() / f".{APP_FOLDER_NAME.lower()}"


def get_default_db_path() -> Path:
    """Caminho padrão (local) usado na primeira execução, antes de o usuário
    configurar uma pasta de rede compartilhada."""
    return get_app_config_dir() / "dados" / DEFAULT_DB_FILE_NAME


def get_config_path() -> Path:
    return get_app_config_dir() / CONFIG_FILE_NAME


def load_config() -> dict:
    config_path = get_config_path()
    if not config_path.exists():
        return {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_config(config: dict) -> None:
    config_dir = get_app_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = get_config_path()
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def get_db_path() -> Path:
    config = load_config()
    saved_path = config.get("db_path")
    if saved_path:
        return Path(saved_path)
    return get_default_db_path()


def set_db_path(new_path: Path) -> None:
    config = load_config()
    config["db_path"] = str(new_path)
    save_config(config)
