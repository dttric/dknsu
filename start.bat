@echo off
title dkn.su Dev Server (Auto-Rebuild + Live-Reload)
echo [*] Starting dkn.su dynamic dev server (auto-rebuild + live-reload)...
cd /d "%~dp0"
python serve.py
pause
