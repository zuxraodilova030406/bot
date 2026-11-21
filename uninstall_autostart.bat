@echo off
chcp 65001 >nul
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_PATH=%STARTUP_DIR%\SarvinozBot.lnk"

if exist "%SHORTCUT_PATH%" (
    del "%SHORTCUT_PATH%"
    echo ✅ Avto-yuklanish muvaffaqiyatli o'chirildi!
) else (
    echo Avto-yuklanish mavjud emas edi.
)

pause
