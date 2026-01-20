@echo off

REM 이 배치가 실행되는 위치를 프로젝트 루트로 맞춤
cd /d "%~dp0\.."

REM 혹시 남아있는 python 프로세스 정리 (선택)
taskkill /IM python.exe /F >nul 2>&1

REM 업데이트
git fetch
git reset --hard origin/main

REM 재실행
python client.py

exit
