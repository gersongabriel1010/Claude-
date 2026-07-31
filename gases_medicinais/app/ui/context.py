"""Contexto compartilhado entre as abas da interface."""
from __future__ import annotations

from pathlib import Path


class AppContext:
    """Guarda o caminho atual do banco de dados e permite que as abas se
    inscrevam para serem atualizadas quando os dados mudam em outra aba."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._listeners = []

    def subscribe(self, callback) -> None:
        self._listeners.append(callback)

    def notify_data_changed(self) -> None:
        for callback in self._listeners:
            callback()

    def set_db_path(self, new_path: Path) -> None:
        self.db_path = new_path
        self.notify_data_changed()
