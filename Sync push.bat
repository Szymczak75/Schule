@echo off
D:
cd "%~dp0"
git pull --no-edit
git add .
git commit -m "Aktualisierung"
git push
pause