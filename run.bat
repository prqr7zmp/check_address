chcp 65001
@echo off
REM 必要な設定と変数
set "VENV_NAME=myenv"

REM 仮想環境をアクティブ化
echo 仮想環境をアクティブ化中...
call %VENV_NAME%\Scripts\activate
if errorlevel 1 (
    echo 仮想環境のアクティブ化に失敗しました。
    exit /b 1
)

REM 仮想環境内でPythonを実行
echo 仮想環境内でPythonを実行中...
python app.py
if errorlevel 1 (
    echo Pythonの実行に失敗しました。
    exit /b 1
)