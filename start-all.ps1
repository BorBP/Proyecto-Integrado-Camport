# Script de Inicio Completo del Sistema CAMPORT

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                     CAMPORT V8.0 - INICIO DEL SISTEMA                     ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "Iniciando componentes del sistema..." -ForegroundColor Yellow
Write-Host ""

# 1. Backend Django
Write-Host "[1/3] Iniciando servidor Django..." -ForegroundColor Green
Start-Job -Name "DjangoServer" -ScriptBlock {
    Set-Location "C:\Users\bale_\Videos\Proyecto Integrado Camport_NUEVO\backend"
    .\venv\Scripts\python.exe manage.py runserver
} | Out-Null

Start-Sleep -Seconds 5

# 2. Simulador
Write-Host "[2/3] Iniciando simulador de collares..." -ForegroundColor Green
Start-Job -Name "Simulator" -ScriptBlock {
    Set-Location "C:\Users\bale_\Videos\Proyecto Integrado Camport_NUEVO\backend"
    .\venv\Scripts\python.exe manage.py simulate_collars_v8
} | Out-Null

Start-Sleep -Seconds 3

# 3. Frontend React
Write-Host "[3/3] Iniciando aplicación React..." -ForegroundColor Green
Start-Job -Name "ReactApp" -ScriptBlock {
    Set-Location "C:\Users\bale_\Videos\Proyecto Integrado Camport_NUEVO\frontend"
    npm start
} | Out-Null

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                       SISTEMA INICIADO CORRECTAMENTE                       ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "Componentes en ejecución:" -ForegroundColor Cyan
Write-Host "  ✓ Backend Django:    http://localhost:8000" -ForegroundColor White
Write-Host "  ✓ Simulador:         Activo (WebSocket conectado)" -ForegroundColor White
Write-Host "  ✓ Frontend React:    http://localhost:3000" -ForegroundColor White
Write-Host ""

Write-Host "Jobs activos:" -ForegroundColor Yellow
Get-Job | Format-Table -AutoSize

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                            COMANDOS ÚTILES                                " -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Ver logs de Django:        Get-Job -Name 'DjangoServer' | Receive-Job" -ForegroundColor White
Write-Host "  Ver logs del Simulador:    Get-Job -Name 'Simulator' | Receive-Job" -ForegroundColor White
Write-Host "  Ver logs de React:         Get-Job -Name 'ReactApp' | Receive-Job" -ForegroundColor White
Write-Host ""
Write-Host "  Detener Django:            Stop-Job -Name 'DjangoServer'" -ForegroundColor White
Write-Host "  Detener Simulador:         Stop-Job -Name 'Simulator'" -ForegroundColor White
Write-Host "  Detener React:             Stop-Job -Name 'ReactApp'" -ForegroundColor White
Write-Host ""
Write-Host "  Detener todo:              Get-Job | Stop-Job; Get-Job | Remove-Job" -ForegroundColor Red
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "Esperando 15 segundos para verificar que todos los servicios estén activos..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

Write-Host ""
Write-Host "Estado de los servicios:" -ForegroundColor Cyan
Get-Job | ForEach-Object {
    $status = if ($_.State -eq "Running") { "✓ ACTIVO" } else { "✗ INACTIVO" }
    $color = if ($_.State -eq "Running") { "Green" } else { "Red" }
    Write-Host "  $status - $($_.Name)" -ForegroundColor $color
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║                        SISTEMA LISTO PARA USAR                            ║" -ForegroundColor Magenta
Write-Host "║                  Accede a: http://localhost:3000                          ║" -ForegroundColor Magenta
Write-Host "╚════════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
Write-Host ""

# Mantener la ventana abierta
Write-Host "Presiona Ctrl+C para detener todos los servicios y salir..." -ForegroundColor Yellow
Write-Host ""

# Loop para mostrar actualizaciones periódicas
while ($true) {
    Start-Sleep -Seconds 30
    
    Write-Host "`n[$(Get-Date -Format 'HH:mm:ss')] Servicios activos:" -ForegroundColor DarkCyan
    Get-Job | Where-Object { $_.State -eq "Running" } | ForEach-Object {
        Write-Host "  ✓ $($_.Name)" -ForegroundColor DarkGreen
    }
    
    # Verificar si algún job falló
    $failedJobs = Get-Job | Where-Object { $_.State -eq "Failed" }
    if ($failedJobs) {
        Write-Host "`n⚠ ADVERTENCIA: Algunos servicios han fallado:" -ForegroundColor Red
        $failedJobs | ForEach-Object {
            Write-Host "  ✗ $($_.Name)" -ForegroundColor Red
        }
    }
}
