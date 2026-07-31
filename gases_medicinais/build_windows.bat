@echo off
REM Script para gerar o executavel (.exe) do Controle de Gases Medicinais
REM no Windows. Execute este arquivo dando duplo clique nele, ou rodando
REM "build_windows.bat" no Prompt de Comando, dentro desta mesma pasta.
REM
REM Pre-requisito: Python 3.10 ou superior instalado no Windows
REM (baixe em https://www.python.org/downloads/ marcando a opcao
REM "Add Python to PATH" durante a instalacao).

echo ============================================
echo  Controle de Gases Medicinais - Build (.exe)
echo ============================================

python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao foi encontrado no PATH do sistema.
    echo Instale o Python em https://www.python.org/downloads/ e marque
    echo a opcao "Add Python to PATH" durante a instalacao.
    pause
    exit /b 1
)

echo.
echo [1/3] Instalando dependencias...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo [2/3] Gerando o executavel com PyInstaller...
python -m PyInstaller --clean --noconfirm gases_medicinais.spec

echo.
echo [3/3] Pronto!
echo O executavel foi gerado em: dist\ControleGasesMedicinais.exe
echo.
pause
