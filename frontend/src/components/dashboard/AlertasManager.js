import React, { useState, useEffect } from 'react';
import { alertaService, reporteService } from '../../services/api';
import './AlertasManager.css';

const AlertasManager = () => {
  const [alertasActivas, setAlertasActivas] = useState([]);
  const [reportes, setReportes] = useState([]);
  const [activeTab, setActiveTab] = useState('activas'); // 'activas' o 'reportes'
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [selectedAlerta, setSelectedAlerta] = useState(null);
  const [observaciones, setObservaciones] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [filtros, setFiltros] = useState({
    fecha_desde: '',
    fecha_hasta: '',
    tipo_alerta: '',
    animal_id: '',
  });

  useEffect(() => {
    loadData();
    // Actualizar cada 10 segundos
    const interval = setInterval(loadData, 10000);
    return () => clearInterval(interval);
  }, [activeTab]);

  const loadData = async () => {
    try {
      if (activeTab === 'activas') {
        const data = await alertaService.getAll();
        setAlertasActivas(data.filter(a => !a.alerta_detalle.resuelta && !a.eliminada));
      } else {
        const data = await reporteService.getAll();
        setReportes(data);
      }
    } catch (error) {
      console.error('Error loading data:', error);
      showMessage('Error al cargar datos', 'error');
    }
  };

  const handleMarcarLeida = async (id) => {
    try {
      await alertaService.marcarLeida(id);
      showMessage('Alerta marcada como leída', 'success');
      loadData();
    } catch (error) {
      console.error('Error:', error);
      showMessage('Error al marcar como leída', 'error');
    }
  };

  const handleEliminar = async (id) => {
    if (!window.confirm('¿Está seguro de eliminar esta alerta?')) return;
    
    try {
      await alertaService.eliminar(id);
      showMessage('Alerta eliminada', 'success');
      loadData();
    } catch (error) {
      console.error('Error:', error);
      showMessage('Error al eliminar alerta', 'error');
    }
  };

  const handleAbrirModal = (alerta) => {
    setSelectedAlerta(alerta);
    setObservaciones('');
    setShowModal(true);
  };

  const handleResolverYReportar = async () => {
    if (!selectedAlerta) return;
    
    try {
      setLoading(true);
      await alertaService.resolverYReportar(selectedAlerta.id, observaciones);
      showMessage('Alerta resuelta y enviada a reportes', 'success');
      setShowModal(false);
      setSelectedAlerta(null);
      setObservaciones('');
      loadData();
    } catch (error) {
      console.error('Error:', error);
      showMessage('Error al resolver alerta', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleExportarCSV = async () => {
    try {
      setLoading(true);
      showMessage('Generando archivo CSV...', 'info');
      await reporteService.exportarCSV();
      showMessage('✓ Archivo CSV descargado correctamente', 'success');
    } catch (error) {
      console.error('Error:', error);
      showMessage('Error al exportar CSV', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleExportarCSVFiltrado = async () => {
    try {
      setLoading(true);
      showMessage('Generando archivo CSV filtrado...', 'info');
      await reporteService.exportarCSVFiltrado(filtros);
      showMessage('✓ Archivo CSV filtrado descargado correctamente', 'success');
    } catch (error) {
      console.error('Error:', error);
      showMessage('Error al exportar CSV filtrado', 'error');
    } finally {
      setLoading(false);
    }
  };

  const showMessage = (msg, type = 'info') => {
    setMessage({ text: msg, type });
    setTimeout(() => setMessage(''), 5000);
  };

  const getTipoIcon = (tipo) => {
    switch (tipo) {
      case 'TEMPERATURA':
        return '🌡️';
      case 'FRECUENCIA':
        return '❤️';
      case 'PERIMETRO':
        return '🚨';
      default:
        return '⚠️';
    }
  };

  const getTipoColor = (tipo) => {
    switch (tipo) {
      case 'TEMPERATURA':
        return '#ff9800';
      case 'FRECUENCIA':
        return '#f44336';
      case 'PERIMETRO':
        return '#2196f3';
      default:
        return '#666';
    }
  };

  const formatFecha = (fecha) => {
    return new Date(fecha).toLocaleString('es-ES', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="alertas-manager">
      <div className="manager-header">
        <h2>📋 Gestión de Alertas y Reportes</h2>
        <div className="tab-buttons">
          <button
            className={`tab-btn ${activeTab === 'activas' ? 'active' : ''}`}
            onClick={() => setActiveTab('activas')}
          >
            🔔 Alertas Activas ({alertasActivas.length})
          </button>
          <button
            className={`tab-btn ${activeTab === 'reportes' ? 'active' : ''}`}
            onClick={() => setActiveTab('reportes')}
          >
            📊 Historial de Reportes ({reportes.length})
          </button>
        </div>
      </div>

      {message && (
        <div className={`message ${message.type}`}>
          {message.text}
          <button onClick={() => setMessage('')}>×</button>
        </div>
      )}

      {activeTab === 'activas' && (
        <div className="alertas-activas-panel">
          <div className="panel-info">
            <p>
              <strong>Panel de Alertas Activas:</strong> Visualiza y gestiona las alertas en tiempo real.
              Puedes marcar como leída, eliminar (si es falso positivo) o resolver y mover a reportes.
            </p>
          </div>

          {alertasActivas.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">✓</div>
              <h3>No hay alertas activas</h3>
              <p>Todas las alertas han sido resueltas</p>
            </div>
          ) : (
            <div className="alertas-grid">
              {alertasActivas.map((alerta) => (
                <div
                  key={alerta.id}
                  className={`alerta-card ${alerta.leido ? 'leida' : 'no-leida'}`}
                  style={{ borderLeftColor: getTipoColor(alerta.alerta_detalle.tipo_alerta) }}
                >
                  <div className="alerta-header">
                    <div className="alerta-icon">
                      {getTipoIcon(alerta.alerta_detalle.tipo_alerta)}
                    </div>
                    <div className="alerta-info">
                      <div className="alerta-tipo">
                        {alerta.alerta_detalle.tipo_alerta}
                      </div>
                      <div className="alerta-animal">
                        {alerta.alerta_detalle.animal_display_id || alerta.alerta_detalle.animal_collar}
                        {!alerta.leido && <span className="badge-new">NUEVA</span>}
                      </div>
                    </div>
                  </div>

                  <div className="alerta-body">
                    <p className="alerta-mensaje">{alerta.alerta_detalle.mensaje}</p>
                    {alerta.alerta_detalle.valor_registrado && (
                      <p className="alerta-valor">
                        <strong>Valor registrado:</strong> {alerta.alerta_detalle.valor_registrado}
                        {alerta.alerta_detalle.tipo_alerta === 'TEMPERATURA' ? '°C' : 
                         alerta.alerta_detalle.tipo_alerta === 'FRECUENCIA' ? ' BPM' : ''}
                      </p>
                    )}
                    <p className="alerta-fecha">
                      {formatFecha(alerta.alerta_detalle.timestamp)}
                    </p>
                  </div>

                  <div className="alerta-actions">
                    {!alerta.leido && (
                      <button
                        className="btn-action btn-leida"
                        onClick={() => handleMarcarLeida(alerta.id)}
                        title="Marcar como leída"
                      >
                        ✓ Marcar Leída
                      </button>
                    )}
                    <button
                      className="btn-action btn-resolver"
                      onClick={() => handleAbrirModal(alerta)}
                      title="Resolver y mover a reportes"
                    >
                      📊 Resolver
                    </button>
                    <button
                      className="btn-action btn-eliminar"
                      onClick={() => handleEliminar(alerta.id)}
                      title="Eliminar (falso positivo)"
                    >
                      🗑️ Eliminar
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'reportes' && (
        <div className="reportes-panel">
          <div className="panel-header">
            <div className="panel-info">
              <p>
                <strong>Historial de Reportes:</strong> Alertas que han sido resueltas.
                Puedes exportarlas en formato CSV para análisis externos.
              </p>
            </div>
            <div className="export-buttons">
              <button
                className="btn-export"
                onClick={handleExportarCSV}
                disabled={loading || reportes.length === 0}
              >
                📥 Exportar Todos (CSV)
              </button>
            </div>
          </div>

          {/* Filtros para exportación */}
          <div className="filtros-panel">
            <h4>Filtros para Exportación:</h4>
            <div className="filtros-grid">
              <div className="filtro-item">
                <label>Desde:</label>
                <input
                  type="date"
                  value={filtros.fecha_desde}
                  onChange={(e) => setFiltros({ ...filtros, fecha_desde: e.target.value })}
                />
              </div>
              <div className="filtro-item">
                <label>Hasta:</label>
                <input
                  type="date"
                  value={filtros.fecha_hasta}
                  onChange={(e) => setFiltros({ ...filtros, fecha_hasta: e.target.value })}
                />
              </div>
              <div className="filtro-item">
                <label>Tipo:</label>
                <select
                  value={filtros.tipo_alerta}
                  onChange={(e) => setFiltros({ ...filtros, tipo_alerta: e.target.value })}
                >
                  <option value="">Todos</option>
                  <option value="TEMPERATURA">Temperatura</option>
                  <option value="FRECUENCIA">Frecuencia</option>
                  <option value="PERIMETRO">Perímetro</option>
                </select>
              </div>
              <div className="filtro-item">
                <button
                  className="btn-export-filtrado"
                  onClick={handleExportarCSVFiltrado}
                  disabled={loading}
                >
                  📥 Exportar Filtrado (CSV)
                </button>
              </div>
            </div>
          </div>

          {reportes.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">📝</div>
              <h3>No hay reportes</h3>
              <p>Los reportes aparecerán cuando resuelvas alertas</p>
            </div>
          ) : (
            <div className="reportes-table">
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Tipo</th>
                    <th>Animal</th>
                    <th>Mensaje</th>
                    <th>Valor</th>
                    <th>Fecha Alerta</th>
                    <th>Fecha Resolución</th>
                    <th>Resuelto Por</th>
                    <th>Exportado</th>
                  </tr>
                </thead>
                <tbody>
                  {reportes.map((reporte) => (
                    <tr key={reporte.id}>
                      <td>#{reporte.id}</td>
                      <td>
                        <span className="tipo-badge" style={{ backgroundColor: getTipoColor(reporte.alerta_detalle.tipo_alerta) }}>
                          {getTipoIcon(reporte.alerta_detalle.tipo_alerta)} {reporte.alerta_detalle.tipo_alerta}
                        </span>
                      </td>
                      <td>
                        {reporte.alerta_detalle.animal_display_id || reporte.alerta_detalle.animal_collar}
                      </td>
                      <td className="mensaje-cell">{reporte.alerta_detalle.mensaje}</td>
                      <td>
                        {reporte.alerta_detalle.valor_registrado ? (
                          <>
                            {reporte.alerta_detalle.valor_registrado}
                            {reporte.alerta_detalle.tipo_alerta === 'TEMPERATURA' ? '°C' :
                             reporte.alerta_detalle.tipo_alerta === 'FRECUENCIA' ? ' BPM' : ''}
                          </>
                        ) : '-'}
                      </td>
                      <td>{formatFecha(reporte.alerta_detalle.timestamp)}</td>
                      <td>
                        {reporte.alerta_detalle.fecha_resolucion 
                          ? formatFecha(reporte.alerta_detalle.fecha_resolucion)
                          : '-'}
                      </td>
                      <td>{reporte.generado_por_username || '-'}</td>
                      <td>
                        {reporte.exportado ? (
                          <span className="exportado-badge">✓ Exportado</span>
                        ) : (
                          <span className="no-exportado-badge">Pendiente</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* Modal para resolver alerta */}
      {showModal && selectedAlerta && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Resolver Alerta</h3>
            <div className="modal-body">
              <div className="alerta-summary">
                <p><strong>Tipo:</strong> {selectedAlerta.alerta_detalle.tipo_alerta}</p>
                <p><strong>Animal:</strong> {selectedAlerta.alerta_detalle.animal_display_id || selectedAlerta.alerta_detalle.animal_collar}</p>
                <p><strong>Mensaje:</strong> {selectedAlerta.alerta_detalle.mensaje}</p>
                {selectedAlerta.alerta_detalle.valor_registrado && (
                  <p>
                    <strong>Valor:</strong> {selectedAlerta.alerta_detalle.valor_registrado}
                    {selectedAlerta.alerta_detalle.tipo_alerta === 'TEMPERATURA' ? '°C' :
                     selectedAlerta.alerta_detalle.tipo_alerta === 'FRECUENCIA' ? ' BPM' : ''}
                  </p>
                )}
              </div>

              <div className="form-group">
                <label>Observaciones (opcional):</label>
                <textarea
                  value={observaciones}
                  onChange={(e) => setObservaciones(e.target.value)}
                  placeholder="Ingrese observaciones sobre la resolución de esta alerta..."
                  rows="4"
                />
              </div>

              <div className="modal-info">
                <p>
                  ℹ️ Al resolver esta alerta, se marcará como resuelta y se moverá al historial de reportes.
                  Podrás exportarla posteriormente en formato CSV.
                </p>
              </div>
            </div>

            <div className="modal-actions">
              <button
                className="btn-confirm"
                onClick={handleResolverYReportar}
                disabled={loading}
              >
                {loading ? 'Procesando...' : '✓ Resolver y Reportar'}
              </button>
              <button
                className="btn-cancel"
                onClick={() => setShowModal(false)}
                disabled={loading}
              >
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AlertasManager;
