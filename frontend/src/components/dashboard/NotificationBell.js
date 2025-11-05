import React, { useState, useEffect } from 'react';
import { alertaService } from '../../services/api';
import './NotificationBell.css';

const NotificationBell = () => {
  const [alertas, setAlertas] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [noLeidas, setNoLeidas] = useState(0);

  useEffect(() => {
    loadAlertas();
    const interval = setInterval(loadAlertas, 10000); // Actualizar cada 10 segundos
    return () => clearInterval(interval);
  }, []);

  const loadAlertas = async () => {
    try {
      const [todasAlertas, alertasNoLeidas] = await Promise.all([
        alertaService.getAll(),
        alertaService.getNoLeidas()
      ]);
      setAlertas(todasAlertas);
      setNoLeidas(alertasNoLeidas.length);
    } catch (error) {
      console.error('Error loading alertas:', error);
    }
  };

  const marcarLeida = async (id) => {
    try {
      await alertaService.marcarLeida(id);
      loadAlertas();
    } catch (error) {
      console.error('Error marking alerta as read:', error);
    }
  };

  const getTipoColor = (tipo) => {
    switch(tipo) {
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

  return (
    <div className="notification-bell">
      <button
        className="bell-button"
        onClick={() => setShowDropdown(!showDropdown)}
      >
        🔔
        {noLeidas > 0 && <span className="badge">{noLeidas}</span>}
      </button>

      {showDropdown && (
        <div className="notification-dropdown">
          <div className="dropdown-header">
            <h4>Notificaciones</h4>
            <button onClick={() => setShowDropdown(false)}>×</button>
          </div>
          <div className="notification-list">
            {alertas.length === 0 ? (
              <div className="no-notifications">No hay notificaciones</div>
            ) : (
              alertas.slice(0, 10).map((alerta) => (
                <div
                  key={alerta.id}
                  className={`notification-item ${alerta.leido ? 'read' : 'unread'}`}
                >
                  <div
                    className="tipo-indicator"
                    style={{ backgroundColor: getTipoColor(alerta.alerta_detalle.tipo_alerta) }}
                  ></div>
                  <div className="notification-content">
                    <strong>{alerta.alerta_detalle.animal_collar}</strong>
                    <p>{alerta.alerta_detalle.mensaje}</p>
                    <small>{new Date(alerta.alerta_detalle.timestamp).toLocaleString()}</small>
                  </div>
                  {!alerta.leido && (
                    <button
                      className="btn-mark-read"
                      onClick={() => marcarLeida(alerta.id)}
                    >
                      ✓
                    </button>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default NotificationBell;
