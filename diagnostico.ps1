# Script de diagnóstico del sistema CAMPORT
# Este script verifica que todo esté configurado correctamente

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🔍 DIAGNÓSTICO DEL SISTEMA CAMPORT V6.0" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$errores = 0
$advertencias = 0

# 1. Verificar Python
Write-Host "1️⃣  Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✅ Python instalado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Python NO encontrado. Instala Python 3.8+" -ForegroundColor Red
    $errores++
}

# 2. Verificar Node.js
Write-Host "2️⃣  Verificando Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "   ✅ Node.js instalado: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Node.js NO encontrado. Instala Node.js 14+" -ForegroundColor Red
    $errores++
}

# 3. Verificar npm
Write-Host "3️⃣  Verificando npm..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version 2>&1
    Write-Host "   ✅ npm instalado: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ npm NO encontrado" -ForegroundColor Red
    $errores++
}

# 4. Verificar entorno virtual backend
Write-Host "4️⃣  Verificando entorno virtual Python..." -ForegroundColor Yellow
if (Test-Path "backend\venv") {
    Write-Host "   ✅ Entorno virtual creado" -ForegroundColor Green
    
    # Verificar Django instalado
    if (Test-Path "backend\venv\Lib\site-packages\django") {
        Write-Host "   ✅ Django instalado en venv" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Django NO instalado. Ejecuta: cd backend && .\venv\Scripts\Activate.ps1 && pip install -r requirements.txt" -ForegroundColor Yellow
        $advertencias++
    }
} else {
    Write-Host "   ⚠️  Entorno virtual NO creado. Ejecuta: cd backend && python -m venv venv" -ForegroundColor Yellow
    $advertencias++
}

# 5. Verificar node_modules frontend
Write-Host "5️⃣  Verificando dependencias frontend..." -ForegroundColor Yellow
if (Test-Path "frontend\node_modules") {
    Write-Host "   ✅ Dependencias npm instaladas" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Dependencias npm NO instaladas. Ejecuta: cd frontend && npm install" -ForegroundColor Yellow
    $advertencias++
}

# 6. Verificar base de datos
Write-Host "6️⃣  Verificando base de datos..." -ForegroundColor Yellow
if (Test-Path "backend\db.sqlite3") {
    $dbSize = (Get-Item "backend\db.sqlite3").Length
    if ($dbSize -gt 10000) {
        Write-Host "   ✅ Base de datos creada ($([math]::Round($dbSize/1KB, 2)) KB)" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Base de datos vacía o corrupta. Ejecuta: cd backend && python populate_db.py" -ForegroundColor Yellow
        $advertencias++
    }
} else {
    Write-Host "   ⚠️  Base de datos NO creada. Ejecuta: cd backend && python manage.py migrate && python populate_db.py" -ForegroundColor Yellow
    $advertencias++
}

# 7. Verificar puertos disponibles
Write-Host "7️⃣  Verificando puertos..." -ForegroundColor Yellow
$puerto8000 = Test-NetConnection -ComputerName localhost -Port 8000 -InformationLevel Quiet -WarningAction SilentlyContinue 2>$null
$puerto3000 = Test-NetConnection -ComputerName localhost -Port 3000 -InformationLevel Quiet -WarningAction SilentlyContinue 2>$null

if ($puerto8000) {
    Write-Host "   ⚠️  Puerto 8000 YA está en uso (Backend puede estar corriendo)" -ForegroundColor Yellow
} else {
    Write-Host "   ✅ Puerto 8000 disponible" -ForegroundColor Green
}

if ($puerto3000) {
    Write-Host "   ⚠️  Puerto 3000 YA está en uso (Frontend puede estar corriendo)" -ForegroundColor Yellow
} else {
    Write-Host "   ✅ Puerto 3000 disponible" -ForegroundColor Green
}

# 8. Verificar archivos esenciales
Write-Host "8️⃣  Verificando archivos del proyecto..." -ForegroundColor Yellow
$archivosEsenciales = @(
    "backend\manage.py",
    "backend\requirements.txt",
    "backend\populate_db.py",
    "frontend\package.json",
    "start-backend.ps1",
    "start-frontend.ps1",
    "start-simulator.ps1",
    "DOCUMENTACION.md"
)

$archivosFaltantes = 0
foreach ($archivo in $archivosEsenciales) {
    if (!(Test-Path $archivo)) {
        Write-Host "   ❌ Falta archivo: $archivo" -ForegroundColor Red
        $archivosFaltantes++
    }
}

if ($archivosFaltantes -eq 0) {
    Write-Host "   ✅ Todos los archivos esenciales presentes" -ForegroundColor Green
} else {
    Write-Host "   ❌ Faltan $archivosFaltantes archivos esenciales" -ForegroundColor Red
    $errores++
}

# Resumen
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "📊 RESUMEN DEL DIAGNÓSTICO" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if ($errores -eq 0 -and $advertencias -eq 0) {
    Write-Host "🎉 ¡Sistema completamente configurado y listo!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Para iniciar el sistema:" -ForegroundColor White
    Write-Host "  1. Backend:    .\start-backend.ps1" -ForegroundColor Cyan
    Write-Host "  2. Frontend:   .\start-frontend.ps1" -ForegroundColor Cyan
    Write-Host "  3. Simulador:  .\start-simulator.ps1" -ForegroundColor Cyan
} elseif ($errores -eq 0) {
    Write-Host "⚠️  Sistema funcional con $advertencias advertencia(s)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Revisa las advertencias arriba y corrígelas si es necesario." -ForegroundColor White
} else {
    Write-Host "❌ Sistema con $errores error(es) y $advertencias advertencia(s)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Debes corregir los errores antes de iniciar el sistema." -ForegroundColor White
    Write-Host "Consulta DOCUMENTACION.md para ayuda." -ForegroundColor White
}

Write-Host ""
Write-Host "📖 Documentación completa: DOCUMENTACION.md" -ForegroundColor Cyan
Write-Host ""
