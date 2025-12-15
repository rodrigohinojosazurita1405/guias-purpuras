@echo off
echo ========================================
echo   Guias Purpuras - Entorno de Desarrollo
echo ========================================
echo.
echo Activando entorno virtual...
call env\Scripts\activate
echo.
echo Cambiando a directorio backend...
cd backend
echo.
echo ========================================
echo   Listo! Ahora puedes usar Django:
echo   - python manage.py runserver
echo   - python manage.py check
echo   - python manage.py migrate
echo ========================================
echo.
