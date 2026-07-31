"""Ponto de entrada do Controle de Gases Medicinais."""
from __future__ import annotations

import sys
import traceback
from tkinter import messagebox

from app import config as app_config


def main() -> None:
    db_path = app_config.get_db_path()
    try:
        from app.ui.main_window import iniciar_app
        root = iniciar_app(db_path)
        root.mainloop()
    except Exception:
        erro = traceback.format_exc()
        try:
            messagebox.showerror("Erro inesperado", f"Ocorreu um erro inesperado:\n\n{erro}")
        except Exception:
            print(erro, file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
