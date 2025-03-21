chcp 65001
@echo off
REM 必要な設定と変数
set "PYTHON_URL=https://www.python.org/ftp/python/3.12.5/python-3.12.5-amd64.exe"
set "PYTHON_INSTALLER=python_installer.exe"
set "VENV_NAME=myenv"
set "REQUIRED_LIBRARIES=flask flask_sqlalchemy flask_cors pyyaml"

REM Pythonをダウンロード
echo Pythonをダウンロード中...
curl -o %PYTHON_INSTALLER% %PYTHON_URL%
if errorlevel 1 (
    echo Pythonのダウンロードに失敗しました。
    exit /b 1
)

REM Pythonをインストール
echo Pythonをインストール中...
start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1
if errorlevel 1 (
    echo Pythonのインストールに失敗しました。
    exit /b 1
)

REM インストールされたPythonの確認
python --version >nul 2>&1
if errorlevel 1 (
    echo Pythonが正しくインストールされていません。
    exit /b 1
)

REM 仮想環境の作成
echo 仮想環境を作成中...
python -m venv %VENV_NAME%
if errorlevel 1 (
    echo 仮想環境の作成に失敗しました。
    exit /b 1
)

REM 仮想環境をアクティブ化
echo 仮想環境をアクティブ化中...
call %VENV_NAME%\Scripts\activate
if errorlevel 1 (
    echo 仮想環境のアクティブ化に失敗しました。
    exit /b 1
)

REM 必要なライブラリをインストール
echo 必要なライブラリをインストール中...
pip install %REQUIRED_LIBRARIES%
if errorlevel 1 (
    echo ライブラリのインストールに失敗しました。
    exit /b 1
)

echo 全ての処理が完了しました。
exit /b 0
