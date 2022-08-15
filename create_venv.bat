@echo off

call conda create --prefix venv\ python=3.8 || pause && exit /b
call conda activate venv\ || pause && exit /b

call conda install pywin32
call python -m pip install --upgrade pip || pause && exit /b
call pip install -r requirements.txt || pause && exit /b
