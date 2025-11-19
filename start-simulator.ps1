# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║              CAMPORT - SCRIPT UNIFICADO DE SIMULADORES                       ║
# ║                         Versiones: V6, V7, V8                                ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

param(
    [Parameter(Position=0)]
    [ValidateSet("v6", "v7", "v8", "6", "7", "8")]
    [string]$Version = "v8",
    
    [int]$Interval = 20,
    [int]$IntervalMovement = 3,
    [int]$IntervalTemperature = 5,
    [int]$IntervalBpm = 2,
    [string]$BlackSheep = "",
    [switch]$Help
)

if ($Help) {
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  CAMPORT - Simulador de Telemetría de Ganado" -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "USO:" -ForegroundColor Yellow
    Write-Host "  .\start-simulator.ps1 [version] [opciones]" -ForegroundColor White
    Write-Host ""
    Write-Host "VERSIONES DISPONIBLES:" -ForegroundColor Yellow
    Write-Host "  v6 (o 6)  - Gravedad de Centroide" -ForegroundColor White
    Write-Host "              • Movimiento con atracción al centro" -ForegroundColor Gray
    Write-Host "              • Sistema de fugas aleatorias" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  v7 (o 7)  - Random Walk Natural + Oveja Negra" -ForegroundColor White
    Write-Host "              • Movimiento 100% errático" -ForegroundColor Gray
    Write-Host "              • Oveja negra específica" -ForegroundColor Gray
    Write-Host "              • Adaptabilidad dinámica" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  v8 (o 8)  - Signos Vitales + Intervalos Independientes [DEFAULT]" -ForegroundColor Green
    Write-Host "              • Temperatura y BPM con variación gradual" -ForegroundColor Gray
    Write-Host "              • Intervalos independientes" -ForegroundColor Gray
    Write-Host "              • Alertas inteligentes" -ForegroundColor Gray
    Write-Host "              • Sistema de cooldown" -ForegroundColor Gray
    Write-Host ""
    Write-Host "OPCIONES:" -ForegroundColor Yellow
    Write-Host "  -Interval N               Intervalo general en segundos (v6, v7)" -ForegroundColor White
    Write-Host "  -IntervalMovement N       Intervalo de movimiento (v8, default: 3)" -ForegroundColor White
    Write-Host "  -IntervalTemperature N    Intervalo de temperatura (v8, default: 5)" -ForegroundColor White
    Write-Host "  -IntervalBpm N            Intervalo de BPM (v8, default: 2)" -ForegroundColor White
    Write-Host "  -BlackSheep ID            ID de la oveja negra (v7, v8)" -ForegroundColor White
    Write-Host "  -Help                     Muestra esta ayuda" -ForegroundColor White
    Write-Host ""
    Write-Host "EJEMPLOS:" -ForegroundColor Yellow
    Write-Host "  .\start-simulator.ps1                    # V8 con valores por defecto" -ForegroundColor Gray
    Write-Host "  .\start-simulator.ps1 v7                 # V7 Random Walk" -ForegroundColor Gray
    Write-Host "  .\start-simulator.ps1 v8 -IntervalMovement 5  # V8 con mov cada 5s" -ForegroundColor Gray
    Write-Host "  .\start-simulator.ps1 v7 -BlackSheep OVINO-001  # V7 con oveja específica" -ForegroundColor Gray
    Write-Host ""
    exit 0
}

# Normalizar versión
$Version = $Version.ToLower().Replace("v", "")

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║           CAMPORT - Simulador de Telemetría de Ganado           ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Activar entorno virtual
Write-Host "⚙️  Activando entorno virtual..." -ForegroundColor Cyan
Set-Location backend
& .\venv\Scripts\Activate.ps1

Write-Host ""

switch ($Version) {
    "6" {
        Write-Host "🚀 Iniciando Simulador V6.0 - Gravedad de Centroide" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Características:" -ForegroundColor White
        Write-Host "  • Movimiento con atracción al centro (20%)" -ForegroundColor Gray
        Write-Host "  • Sistema de fugas aleatorias" -ForegroundColor Gray
        Write-Host "  • Retorno automático" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Intervalo: $Interval segundos" -ForegroundColor Cyan
        Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Yellow
        Write-Host ""
        
        python manage.py simulate_collars --interval $Interval --gravity-factor 0.2
    }
    
    "7" {
        Write-Host "🚀 Iniciando Simulador V7.0 - Random Walk Natural" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Características:" -ForegroundColor White
        Write-Host "  • Random Walk puro (sin gravedad)" -ForegroundColor Gray
        Write-Host "  • Oveja negra con tendencia a escapar" -ForegroundColor Gray
        Write-Host "  • Adaptabilidad dinámica a geocercas" -ForegroundColor Gray
        Write-Host "  • Reposicionamiento automático" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Intervalo: $Interval segundos" -ForegroundColor Cyan
        if ($BlackSheep) {
            Write-Host "Oveja negra: $BlackSheep" -ForegroundColor Magenta
        }
        Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Yellow
        Write-Host ""
        
        $args = @("--interval", $Interval)
        if ($BlackSheep) {
            $args += @("--black-sheep", $BlackSheep)
        }
        
        python manage.py simulate_collars_v7 @args
    }
    
    "8" {
        Write-Host "🚀 Iniciando Simulador V8.0 - Signos Vitales Realistas" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Características:" -ForegroundColor White
        Write-Host "  ✅ Signos vitales con variación gradual" -ForegroundColor Gray
        Write-Host "  ✅ Intervalos independientes (Mov/Temp/BPM)" -ForegroundColor Gray
        Write-Host "  ✅ Alertas inteligentes (solo con geocerca)" -ForegroundColor Gray
        Write-Host "  ✅ Sistema de cooldown anti-spam diferenciado" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Intervalos:" -ForegroundColor Cyan
        Write-Host "  🚶 Movimiento: $IntervalMovement segundos" -ForegroundColor White
        Write-Host "  🌡️  Temperatura: $IntervalTemperature segundos" -ForegroundColor White
        Write-Host "  ❤️  BPM: $IntervalBpm segundos" -ForegroundColor White
        Write-Host ""
        Write-Host "Cooldowns de alertas:" -ForegroundColor Cyan
        Write-Host "  🌡️❤️  Vitales (Temp/BPM): 180s (3 min)" -ForegroundColor White
        Write-Host "  🚨 Perímetro: 60s (1 min)" -ForegroundColor White
        if ($BlackSheep) {
            Write-Host "  🐑 Oveja negra: $BlackSheep" -ForegroundColor Magenta
        }
        Write-Host ""
        Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Yellow
        Write-Host ""
        
        $args = @(
            "--interval-movement", $IntervalMovement,
            "--interval-temperature", $IntervalTemperature,
            "--interval-bpm", $IntervalBpm
        )
        if ($BlackSheep) {
            $args += @("--black-sheep", $BlackSheep)
        }
        
        python manage.py simulate_collars_v8 @args
    }
    
    default {
        Write-Host "❌ Versión no válida: $Version" -ForegroundColor Red
        Write-Host "Usa: v6, v7, o v8" -ForegroundColor Yellow
        Write-Host "Para ayuda: .\start-simulator.ps1 -Help" -ForegroundColor Cyan
        exit 1
    }
}

Set-Location ..
