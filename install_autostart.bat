@echo off
chcp 65001 >nul
echo 👑 Sarvinoz Collection Bot - Windows Avto-Yuklanish sozlanmoqda...

set "SCRIPT_DIR=%~dp0"
set "VBS_PATH=%SCRIPT_DIR%start_silent.vbs"
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_PATH=%STARTUP_DIR%\SarvinozBot.lnk"

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT_PATH%'); $s.TargetPath = '%VBS_PATH%'; $s.WorkingDirectory = '%SCRIPT_DIR%'; $s.Save()"

echo.
echo ✅ Muvaffaqiyatli sozlandi!
echo Endi kompyuteringiz har gal yoqilganda bot orqa fonda (yashirin) avtomatik ishga tushadi.
echo.
pause
