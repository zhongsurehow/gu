@echo off
chcp 65001 >nul
title 天机变 - 易经主题策略游戏

echo.
echo ========================================
echo    天机变 - 易经主题策略游戏
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.7+
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查是否在正确目录
if not exist "main.py" (
    echo 错误：未找到main.py文件
    echo 请确保在游戏目录中运行此脚本
    pause
    exit /b 1
)

REM 启动游戏
echo 正在启动游戏...
echo.
python launcher.py

REM 游戏结束后暂停
echo.
echo 游戏已结束
pause