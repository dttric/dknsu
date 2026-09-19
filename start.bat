@echo off
title dkn.su Local Server
echo Starting dkn.su local server with 404 support...
cd /d "%~dp0"
python serve.py
pause
