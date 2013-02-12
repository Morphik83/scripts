@echo off
REM :set window size
mode con cols=120 lines=50 >nul
call 
REM :start program
python <your_path_here>\crawler.py
pause