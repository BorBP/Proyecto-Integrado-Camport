import React, { useState, useEffect } from 'react';
import { geocercaService } from '../../services/api';
import './GeofenceEditor.css';

const GeofenceEditor = () => {
  const [geocerca, setGeocerca] = useState(null);
  const [message, setMessage] = useState('');

  useEffect(() => {
    loadGeocerca();
  }, []);

  const loadGeocerca = async () => {
    try {
      const data = await geocercaService.getActiva();
      setGeocerca(data);
    } catch (error) {
      console.log('No hay geocerca activa');
    }
  };

  const handleUpdateCoords = () => {
    setMessage('Actualización de coordenadas desde el mapa aún no implementada. Use las coordenadas por defecto.');
  };

  return (
    <div className="geofence-container">
      <h2>Editor de Geocerca</h2>
      <p className="description">
        La geocerca define el perímetro permitido para el ganado. 
        Los animales que salgan de esta zona generarán alertas automáticas.
      </p>

      {geocerca ? (
        <div className="geofence-info">
          <h3>Geocerca Activa</h3>
          <p><strong>Nombre:</strong> {geocerca.nombre}</p>
          <p><strong>Creado por:</strong> {geocerca.creado_por_username}</p>
          <p><strong>Fecha de creación:</strong> {new Date(geocerca.fecha_creacion).toLocaleDateString()}</p>
          
          <h4>Coordenadas del Perímetro:</h4>
          <div className="coords-list">
            {geocerca.coordenadas.map((coord, index) => (
              <div key={index} className="coord-item">
                <span>Punto {index + 1}:</span>
                <span>Lat: {coord.lat.toFixed(4)}, Lng: {coord.lng.toFixed(4)}</span>
              </div>
            ))}
          </div>

          <div className="geofence-actions">
            <button onClick={handleUpdateCoords} className="btn-update">
              Editar Coordenadas
            </button>
          </div>
        </div>
      ) : (
        <div className="no-geofence">
          <p>⚠️ No hay geocerca activa configurada</p>
          <button onClick={handleUpdateCoords} className="btn-create">
            Crear Nueva Geocerca
          </button>
        </div>
      )}

      {message && (
        <div className="message-info">
          {message}
        </div>
      )}

      <div className="geofence-note">
        <p><strong>Nota:</strong> Para una implementación completa, aquí se integraría un editor de mapa interactivo 
        donde los administradores pueden dibujar polígonos directamente en el mapa usando react-leaflet-draw.</p>
      </div>
    </div>
  );
};

export default GeofenceEditor;
