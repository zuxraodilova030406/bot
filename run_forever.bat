@echo off
chcp 65001 >nul
title Sarvinoz Collection Bot - 24/7 Auto-Restart Watchdog
cd /d "%~dp0"

echo ======================================================
echo 👑 Sarvinoz Collection - 24/7 Avtomatik Qayta Ishga Tushirish
echo ======================================================
echo Bot doimiy rejimda ishlamoqda. Agar internet uzilsa yoki
echo xatolik bo'lsa, tizim 5 soniyada uni avtomatik qayta yoqadi.
echo Oynani yopish orqali to'xtatishingiz mumkin.
echo ======================================================

:restart_loop
echo.
echo [%date% %time%] Bot ishga tushirilmoqda...
python bot.py
echo.
echo [%date% %time%] OGOHLANTIRISH: Bot to'xtadi!
echo 5 soniyadan keyin avtomatik qayta ishga tushiriladi...
timeout /t 5 /nobreak >nul
goto restart_loop
