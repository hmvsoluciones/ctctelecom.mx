@echo off
setlocal
cd /d "%~dp0"
set "PORT=8080"
if not "%~1"=="" set "PORT=%~1"

echo.
echo ============================================
echo   CTC Telecom - vista local del sitio
echo ============================================
echo.

rem 1) Hugo instalado en el PATH
where hugo >nul 2>nul
if %errorlevel%==0 (
  echo Sirviendo con Hugo en http://localhost:%PORT%/
  if not defined NO_OPEN start "" cmd /c "timeout /t 2 >nul ^& start http://localhost:%PORT%/"
  hugo server --port %PORT% --disableFastRender
  goto :eof
)

rem 2) Binario local de este equipo (..\.tools\hugo\hugo.exe)
if exist "..\.tools\hugo\hugo.exe" (
  echo Sirviendo con el Hugo local en http://localhost:%PORT%/
  if not defined NO_OPEN start "" cmd /c "timeout /t 2 >nul ^& start http://localhost:%PORT%/"
  "..\.tools\hugo\hugo.exe" server --port %PORT% --disableFastRender
  goto :eof
)

rem 3) Python: sirve la carpeta ya compilada (public\)
where python >nul 2>nul
if %errorlevel%==0 (
  echo Sirviendo public\ en http://localhost:%PORT%/
  if not defined NO_OPEN start "" cmd /c "timeout /t 2 >nul ^& start http://localhost:%PORT%/"
  python -m http.server %PORT% --directory public
  goto :eof
)

where py >nul 2>nul
if %errorlevel%==0 (
  echo Sirviendo public\ en http://localhost:%PORT%/
  if not defined NO_OPEN start "" cmd /c "timeout /t 2 >nul ^& start http://localhost:%PORT%/"
  py -3 -m http.server %PORT% --directory public
  goto :eof
)

echo.
echo No se encontro Hugo ni Python.
echo Instala Hugo (winget install Hugo.Hugo) o Python y vuelve a ejecutar este archivo.
echo.
pause
exit /b 1
