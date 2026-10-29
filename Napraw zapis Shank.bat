@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
python "%~dp0tools\napraw_zapis.py"
pause
