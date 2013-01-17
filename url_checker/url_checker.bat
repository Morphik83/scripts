@echo off
REM :set window size
mode con cols=120 lines=50 >nul
call 
REM :start program
python <path_to_url_checker_module>\url_checker.py
pause