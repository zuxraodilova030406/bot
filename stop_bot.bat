@echo off
chcp 65001 >nul
echo 🛑 Sarvinoz Collection bot to'xtatilmoqda...
taskkill /F /FI "WINDOWTITLE eq Sarvinoz Collection Bot*" >nul 2>&1
wmic process where "commandline like '%%bot.py%%'" delete >nul 2>&1
echo ✅ Bot muvaffaqiyatli to'xtatildi.
pause
