# Script para iniciar el backend Django

Write-Host "🚀 Iniciando Backend Django..." -ForegroundColor Green
Write-Host ""

Set-Location backend
.\venv\Scripts\Activate.ps1

Write-Host "📡 Backend estará disponible en: http://localhost:8000" -ForegroundColor Cyan
Write-Host "🔧 Panel Admin: http://localhost:8000/admin" -ForegroundColor Cyan
Write-Host ""

python manage.py runserver
