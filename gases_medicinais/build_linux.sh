#!/bin/bash
# Script para gerar o executavel do Controle de Gases Medicinais no Linux.
# (o hospital usa Windows; este script serve apenas para desenvolvimento/teste)
set -e
cd "$(dirname "$0")"
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m PyInstaller --clean --noconfirm gases_medicinais.spec
echo "Executavel gerado em: dist/ControleGasesMedicinais"
