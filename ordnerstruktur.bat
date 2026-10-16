@echo off
rem Erstellt eine Liste aller Ordner und HTML-Seiten in diesem Ordner.
rem In den Ordner "Github-Schule" legen und doppelklicken.
rem Ergebnis: ordnerstruktur.txt im selben Ordner.
chcp 65001 >nul
cd /d "%~dp0"
(
  echo Grundordner: %CD%
  echo.
  echo === Ordner ===
  dir /s /b /ad | findstr /v /i /l /c:".git"
  echo.
  echo === HTML-Seiten ===
  dir /s /b /a-d *.html | findstr /v /i /l /c:".git"
) > ordnerstruktur.txt
echo Fertig: ordnerstruktur.txt wurde erstellt.
pause
