@echo off
echo ==========================================
echo Configurando el Proyecto Marichuy...
echo ==========================================
echo.
echo Creando entorno virtual...
python -m venv venv
echo.
echo Instalando dependencias...
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo.
echo ==========================================
echo Todo listo. Iniciando el servidor...
echo (Puedes abrir en tu navegador: http://127.0.0.1:5000)
echo ==========================================
python run.py
pause
