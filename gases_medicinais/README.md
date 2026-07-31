# Controle de Gases Medicinais

Aplicativo desktop (Python + Tkinter + SQLite) para controle de entrada e
saída de materiais de gases medicinais em um hospital. Veja o manual de
uso completo em [`docs/MANUAL.md`](docs/MANUAL.md).

## Stack

- **Python 3.11+** com **Tkinter** (interface gráfica nativa, sem
  dependências pesadas).
- **SQLite** (`sqlite3`, embutido no Python) como banco de dados em
  arquivo único, configurável para pasta local ou de rede.
- **openpyxl** para exportação em Excel.
- **PyInstaller** para gerar o executável.

## Estrutura

```
gases_medicinais/
├── app/
│   ├── main.py            # ponto de entrada
│   ├── config.py          # configuração local (caminho do banco)
│   ├── db.py               # acesso ao banco de dados (SQLite)
│   ├── export.py          # exportação CSV/Excel
│   └── ui/                # telas (Tkinter)
├── tests/
│   └── test_app_flow.py   # testes funcionais de ponta a ponta
├── run_app.py              # script de entrada (dev e PyInstaller)
├── gases_medicinais.spec  # configuração do PyInstaller
├── build_windows.bat      # gera o .exe no Windows
├── build_linux.sh         # gera o executável no Linux (dev/teste)
└── requirements.txt
```

## Rodando em modo desenvolvimento

```bash
pip install -r requirements.txt
python run_app.py
```

## Rodando os testes

```bash
pip install -r requirements.txt pytest
python -m pytest tests/ -v
```

(em ambiente Linux sem interface gráfica, use `xvfb-run -a` antes do
comando de teste)

## Gerando o executável

No Windows, veja a seção 1 do [manual de uso](docs/MANUAL.md). Em
resumo: instale o Python e rode `build_windows.bat`.
