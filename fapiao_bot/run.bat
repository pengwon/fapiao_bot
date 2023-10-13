@echo off
SETLOCAL

:: 获取当前脚本文件的路径
for %%I in ("%~dp0.") do set "SCRIPT_PATH=%%~fI"

:: 设置当前工作目录为脚本文件所在的目录
cd /d "%SCRIPT_PATH%"

:: 设置虚拟环境中的Python解释器路径（相对路径）
set PYTHON_EXECUTABLE=..\venv\python.exe

:: 执行Python脚本（假设主程序是 run_bot.py）
%PYTHON_EXECUTABLE% run_bot.py >> log.txt

ENDLOCAL
