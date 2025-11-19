# Script de Limpieza de Servicios CAMPORT
# Detiene todos los servicios relacionados con el proyecto

Write-Host "╔════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Red
Write-Host "║                   LIMPIEZA DE SERVICIOS CAMPORT                           ║" -ForegroundColor Red
Write-Host "╚════════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Red
Write-Host ""

Write-Host "Este script detendrá:" -ForegroundColor Yellow
Write-Host "  - Todos los jobs de PowerShell" -ForegroundColor White
Write-Host "  - Procesos Python relacionados con Django/Simulador" -ForegroundColor White
Write-Host "  - Procesos Node relacionados con React" -ForegroundColor White
Write-Host ""

$response = Read-Host "¿Deseas continuar? (S/N)"
if ($response -ne "S" -and $response -ne "s") {
    Write-Host "Operación cancelada" -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                         LIMPIANDO JOBS                                    " -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$jobs = Get-Job -ErrorAction SilentlyContinue
if ($jobs) {
    Write-Host "Deteniendo $($jobs.Count) job(s)..." -ForegroundColor Yellow
    Get-Job | Stop-Job -ErrorAction SilentlyContinue
    Get-Job | Remove-Job -Force -ErrorAction SilentlyContinue
    Write-Host "✓ Jobs limpiados" -ForegroundColor Green
} else {
    Write-Host "✓ No hay jobs activos" -ForegroundColor Green
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                     LIMPIANDO PROCESOS PYTHON                             " -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    Write-Host "Encontrados $($pythonProcesses.Count) proceso(s) Python:" -ForegroundColor Yellow
    $pythonProcesses | ForEach-Object {
        Write-Host "  - PID $($_.Id) - Memoria: $([math]::Round($_.WorkingSet64/1MB,2)) MB" -ForegroundColor White
    }
    
    Write-Host ""
    $killPython = Read-Host "¿Detener procesos Python? (S/N)"
    if ($killPython -eq "S" -or $killPython -eq "s") {
        $pythonProcesses | ForEach-Object {
            Write-Host "  Deteniendo PID $($_.Id)..." -ForegroundColor Yellow
            Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
        }
        Write-Host "✓ Procesos Python detenidos" -ForegroundColor Green
    } else {
        Write-Host "⊘ Procesos Python NO detenidos" -ForegroundColor Yellow
    }
} else {
    Write-Host "✓ No hay procesos Python activos" -ForegroundColor Green
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                      LIMPIANDO PROCESOS NODE                              " -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$nodeProcesses = Get-Process node -ErrorAction SilentlyContinue
if ($nodeProcesses) {
    Write-Host "Encontrados $($nodeProcesses.Count) proceso(s) Node:" -ForegroundColor Yellow
    $nodeProcesses | ForEach-Object {
        Write-Host "  - PID $($_.Id) - Memoria: $([math]::Round($_.WorkingSet64/1MB,2)) MB" -ForegroundColor White
    }
    
    Write-Host ""
    $killNode = Read-Host "¿Detener procesos Node? (S/N)"
    if ($killNode -eq "S" -or $killNode -eq "s") {
        $nodeProcesses | ForEach-Object {
            Write-Host "  Deteniendo PID $($_.Id)..." -ForegroundColor Yellow
            Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
        }
        Write-Host "✓ Procesos Node detenidos" -ForegroundColor Green
    } else {
        Write-Host "⊘ Procesos Node NO detenidos" -ForegroundColor Yellow
    }
} else {
    Write-Host "✓ No hay procesos Node activos" -ForegroundColor Green
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                      VERIFICACIÓN FINAL                                   " -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Start-Sleep -Seconds 2

# Verificar puertos
$port8000 = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
$port3000 = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue

if ($port8000) {
    Write-Host "⚠ Puerto 8000 todavía está ocupado" -ForegroundColor Yellow
} else {
    Write-Host "✓ Puerto 8000 liberado" -ForegroundColor Green
}

if ($port3000) {
    Write-Host "⚠ Puerto 3000 todavía está ocupado" -ForegroundColor Yellow
} else {
    Write-Host "✓ Puerto 3000 liberado" -ForegroundColor Green
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                          LIMPIEZA COMPLETADA                              ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "Ahora puedes ejecutar: .\start-all.ps1" -ForegroundColor Cyan
Write-Host ""
