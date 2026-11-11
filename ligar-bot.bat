@echo off
chcp 65001 >nul
title Central Sao Paulo Bot
cd /d "%~dp0"
python bot.py
pause
