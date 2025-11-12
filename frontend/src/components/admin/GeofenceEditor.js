import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Polygon, Marker, Popup, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import { geocercaService } from '../../services/api';
import './GeofenceEditor.css';

// Fix para los iconos de Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const GeofenceEditor = () => {
  const [geocercas, setGeocercas] = useState([]);
  const [selectedGeofence, setSelectedGeofence] = useState(null);
  const [editingVertex, setEditingVertex] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [newCoord, setNewCoord] = useState(null);
  const [message, setMessage] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newGeofenceName, setNewGeofenceName] = useState('');

  useEffect(() => {
    loadGeocercas();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadGeocercas = async () => {
    try {
      const data = await geocercaService.getAll();
      setGeocercas(data);
      if (data.length > 0 && !selectedGeofence) {
        setSelectedGeofence(data[0]);
      }
    } catch (error) {
      console.error('Error loading geocercas:', error);
    }
  };

  const handleVertexClick = (index) => {
    setEditingVertex(index);
    setShowModal(true);
    setNewCoord(null);
  };

  const handleMapClick = (latlng) => {
    setNewCoord(latlng);
  };

  const handleSaveVertex = async () => {
    if (!newCoord || editingVertex === null) return;

    try {
      const updatedCoords = [...selectedGeofence.coordenadas];
      updatedCoords[editingVertex] = { lat: newCoord.lat, lng: newCoord.lng };

      await geocercaService.update(selectedGeofence.id, {
        ...selectedGeofence,
        coordenadas: updatedCoords
      });

      setMessage('Vértice actualizado correctamente');
      setShowModal(false);
      setEditingVertex(null);
      setNewCoord(null);
      loadGeocercas();
    } catch (error) {
      setMessage('Error al actualizar el vértice');
      console.error(error);
    }
  };

  const handleCreateGeofence = async () => {
    if (!newGeofenceName.trim()) {
      alert('Ingrese un nombre para la geocerca');
      return;
    }

    try {
      // Coordenadas por defecto para una nueva geocerca
      const defaultCoords = [
        { lat: -38.8440, lng: -72.2946 },
        { lat: -38.8450, lng: -72.2946 },
        { lat: -38.8450, lng: -72.2936 },
        { lat: -38.8440, lng: -72.2936 }
      ];

      await geocercaService.create({
        nombre: newGeofenceName,
        coordenadas: defaultCoords,
        activa: true
      });

      setMessage('Geocerca creada correctamente');
      setShowCreateForm(false);
      setNewGeofenceName('');
      loadGeocercas();
    } catch (error) {
      setMessage('Error al crear la geocerca');
      console.error(error);
    }
  };

  const handleDeleteGeofence = async (id) => {
    if (!window.confirm('¿Está seguro de eliminar esta geocerca?')) return;

    try {
      await geocercaService.delete(id);
      setMessage('Geocerca eliminada correctamente');
      setSelectedGeofence(null);
      loadGeocercas();
    } catch (error) {
      setMessage('Error al eliminar la geocerca');
      console.error(error);
    }
  };

  const handleToggleActive = async (geocerca) => {
    try {
      await geocercaService.update(geocerca.id, {
        ...geocerca,
        activa: !geocerca.activa
      });
      setMessage(`Geocerca ${geocerca.activa ? 'desactivada' : 'activada'} correctamente`);
      loadGeocercas();
    } catch (error) {
      setMessage('Error al cambiar el estado de la geocerca');
      console.error(error);
    }
  };

  return (
    <div className="geofence-container">
      <h2>Editor de Geocercas - CAMPORT</h2>
      <p className="description">
        Gestione las geocercas del sistema. Puede crear múltiples geocercas, editarlas y asignarlas a animales.
      </p>

      <div className="geofence-controls">
        <div className="geofence-list">
          <h3>Geocercas Disponibles ({geocercas.length})</h3>
          <button 
            onClick={() => setShowCreateForm(!showCreateForm)} 
            className="btn-create"
          >
            + Nueva Geocerca
          </button>

          {showCreateForm && (
            <div className="create-form">
              <input
                type="text"
                placeholder="Nombre de la geocerca"
                value={newGeofenceName}
                onChange={(e) => setNewGeofenceName(e.target.value)}
              />
              <div>
                <button onClick={handleCreateGeofence} className="btn-save">Crear</button>
                <button onClick={() => setShowCreateForm(false)} className="btn-cancel">Cancelar</button>
              </div>
            </div>
          )}

          <div className="geocercas-grid">
            {geocercas.map(g => (
              <div 
                key={g.id} 
                className={`geocerca-card ${selectedGeofence?.id === g.id ? 'selected' : ''}`}
                onClick={() => setSelectedGeofence(g)}
              >
                <h4>{g.nombre}</h4>
                <p>Animales: {g.animales_count || 0}</p>
                <p>Estado: <span className={`badge ${g.activa ? 'active' : 'inactive'}`}>
                  {g.activa ? 'Activa' : 'Inactiva'}
                </span></p>
                <p>Puntos: {g.coordenadas?.length || 0}</p>
                <div className="card-actions">
                  <button 
                    onClick={(e) => { e.stopPropagation(); handleToggleActive(g); }}
                    className="btn-toggle"
                  >
                    {g.activa ? '🔴 Desactivar' : '🟢 Activar'}
                  </button>
                  <button 
                    onClick={(e) => { e.stopPropagation(); handleDeleteGeofence(g.id); }}
                    className="btn-delete"
                  >
                    🗑️ Eliminar
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {selectedGeofence && (
          <div className="geofence-editor">
            <h3>Editando: {selectedGeofence.nombre}</h3>
            <p className="info">Haga clic en un vértice (punto) del polígono para editarlo</p>
            
            <div className="map-editor">
              <MapContainer 
                center={[-38.8444, -72.2946]} 
                zoom={14} 
                style={{ height: '400px', width: '100%' }}
              >
                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                
                <Polygon
                  positions={selectedGeofence.coordenadas.map(c => [c.lat, c.lng])}
                  pathOptions={{ color: 'blue', fillOpacity: 0.2 }}
                />

                {selectedGeofence.coordenadas.map((coord, index) => (
                  <Marker
                    key={index}
                    position={[coord.lat, coord.lng]}
                    eventHandlers={{
                      click: () => handleVertexClick(index)
                    }}
                  >
                    <Popup>
                      Vértice {index + 1}<br/>
                      Lat: {coord.lat.toFixed(4)}<br/>
                      Lng: {coord.lng.toFixed(4)}<br/>
                      <button onClick={() => handleVertexClick(index)}>Editar</button>
                    </Popup>
                  </Marker>
                ))}
              </MapContainer>
            </div>

            <div className="coords-list">
              <h4>Coordenadas del Perímetro:</h4>
              {selectedGeofence.coordenadas.map((coord, index) => (
                <div key={index} className="coord-item">
                  <span>Punto {index + 1}:</span>
                  <span>Lat: {coord.lat.toFixed(4)}, Lng: {coord.lng.toFixed(4)}</span>
                  <button 
                    onClick={() => handleVertexClick(index)}
                    className="btn-edit-vertex"
                  >
                    ✏️ Editar
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {message && (
        <div className="message-info">
          {message}
          <button onClick={() => setMessage('')}>×</button>
        </div>
      )}

      {/* Modal para editar vértice */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Editar Vértice {editingVertex + 1}</h3>
            <p>Haga clic en el mapa para seleccionar la nueva ubicación</p>
            
            <div className="mini-map">
              <MapContainer 
                center={selectedGeofence.coordenadas[editingVertex] 
                  ? [selectedGeofence.coordenadas[editingVertex].lat, selectedGeofence.coordenadas[editingVertex].lng]
                  : [-38.8444, -72.2946]
                } 
                zoom={15} 
                style={{ height: '300px', width: '100%' }}
              >
                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <MapClickHandler onClick={handleMapClick} />
                
                {newCoord && (
                  <Marker position={[newCoord.lat, newCoord.lng]}>
                    <Popup>Nueva ubicación</Popup>
                  </Marker>
                )}
              </MapContainer>
            </div>

            {newCoord && (
              <div className="new-coord-info">
                <p><strong>Nueva coordenada seleccionada:</strong></p>
                <p>Lat: {newCoord.lat.toFixed(6)}, Lng: {newCoord.lng.toFixed(6)}</p>
              </div>
            )}

            <div className="modal-actions">
              <button 
                onClick={handleSaveVertex} 
                className="btn-save"
                disabled={!newCoord}
              >
                Guardar
              </button>
              <button onClick={() => setShowModal(false)} className="btn-cancel">
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Componente auxiliar para capturar clics en el mapa
function MapClickHandler({ onClick }) {
  useMapEvents({
    click(e) {
      onClick(e.latlng);
    },
  });
  return null;
}

export default GeofenceEditor;
