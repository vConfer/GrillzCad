@echo off
cd /d "%~dp0"
if not exist .venv (
  py -m venv .venv
)
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.
echo Usage:
echo python run_segmentation.py "C:\path\to\your_model.stl" outputs --crease-angle 35 --min-faces 100
echo.
pause
