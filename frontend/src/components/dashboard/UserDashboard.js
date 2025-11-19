import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import useWebSocket from '../../hooks/useWebSocket';
import { animalService, geocercaService } from '../../services/api';
import MapComponent from '../map/MapContainer';
import NotificationBell from './NotificationBell';
import AlertasManager from './AlertasManager';
import './UserDashboard.css';

const UserDashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [animales, setAnimales] = useState([]);
  const [geocercas, setGeocercas] = useState([]);
  const [selectedAnimal, setSelectedAnimal] = useState(null);
  const [activeView, setActiveView] = useState('mapa'); // 'mapa' o 'alertas'
  
  const { lastMessage, isConnected } = useWebSocket('ws://localhost:8000/ws/telemetria/');

  useEffect(() => {
    loadData();
  }, []);

  useEffect(() => {
    if (lastMessage) {
      updateAnimalData(lastMessage);
    }
  }, [lastMessage]);

  const loadData = async () => {
    try {
      const [animalesData, geocercasData] = await Promise.all([
        animalService.getAll(),
        geocercaService.getAll().catch(() => [])
      ]);
      
      setAnimales(animalesData);
      setGeocercas(geocercasData);
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  const updateAnimalData = (telemetriaData) => {
    console.log('📡 Telemetría recibida en frontend:', telemetriaData);
    
    setAnimales(prevAnimales => {
      const updated = prevAnimales.map(animal => {
        if (animal.collar_id === telemetriaData.collar_id) {
          console.log(`✅ Actualizando ${animal.collar_id}: (${telemetriaData.latitud}, ${telemetriaData.longitud})`);
          return {
            ...animal,
            latitud: telemetriaData.latitud,
            longitud: telemetriaData.longitud,
            temperatura_corporal: telemetriaData.temperatura_corporal,
            frecuencia_cardiaca: telemetriaData.frecuencia_cardiaca,
          };
        }
        return animal;
      });
      return updated;
    });
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>🐄 CAMPORT - Monitor de Ganado en Tiempo Real</h1>
        <div className="header-actions">
          <div className="connection-status">
            <span className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}></span>
            {isConnected ? 'Conectado' : 'Desconectado'}
          </div>
          
          <div className="view-selector">
            <button 
              className={`view-btn ${activeView === 'mapa' ? 'active' : ''}`}
              onClick={() => setActiveView('mapa')}
            >
              🗺️ Mapa
            </button>
            <button 
              className={`view-btn ${activeView === 'alertas' ? 'active' : ''}`}
              onClick={() => setActiveView('alertas')}
            >
              📋 Alertas/Reportes
            </button>
          </div>
          
          <NotificationBell />
          {user?.is_staff && (
            <button onClick={() => navigate('/admin')} className="btn-admin">
              ⚙️ Admin
            </button>
          )}
          <div className="user-info">
            <span>👤 {user?.username}</span>
            {user?.is_staff && <span className="admin-badge">Admin</span>}
          </div>
          <button onClick={logout} className="btn-logout">Cerrar Sesión</button>
        </div>
      </div>

      <div className="dashboard-content">
        {activeView === 'mapa' ? (
          <>
            <div className="sidebar">
              <h3>Animales Monitoreados ({animales.length})</h3>
              <div className="animal-list">
                {animales.map(animal => (
                  <div
                    key={animal.collar_id}
                    className={`animal-card ${selectedAnimal?.collar_id === animal.collar_id ? 'selected' : ''}`}
                    onClick={() => setSelectedAnimal(animal)}
                  >
                    <div className="animal-emoji">
                      {animal.tipo_animal === 'OVINO' ? '🐑' : animal.tipo_animal === 'BOVINO' ? '🐄' : '🐎'}
                    </div>
                    <div className="animal-info">
                      <strong>{animal.display_id || animal.collar_id}</strong>
                      <p>{animal.tipo_animal} - {animal.raza}</p>
                      {animal.geocerca_nombre && (
                        <p className="geocerca-info">📍 {animal.geocerca_nombre}</p>
                      )}
                      <div className="vitals">
                        <span>🌡️ {animal.temperatura_corporal ? `${animal.temperatura_corporal}°C` : 'N/A'}</span>
                        <span>❤️ {animal.frecuencia_cardiaca ? `${animal.frecuencia_cardiaca} lpm` : 'N/A'}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="map-section">
              <MapComponent
                animales={animales}
                geocercas={geocercas}
                onAnimalClick={setSelectedAnimal}
              />
            </div>

            {selectedAnimal && (
              <div className="details-panel">
                <div className="panel-header">
                  <h3>Detalles del Animal</h3>
                  <button onClick={() => setSelectedAnimal(null)} className="btn-close">×</button>
                </div>
                <div className="panel-content">
                  <h4>{selectedAnimal.display_id || selectedAnimal.collar_id}</h4>
                  <p><strong>Collar ID:</strong> {selectedAnimal.collar_id}</p>
                  <p><strong>Tipo:</strong> {selectedAnimal.tipo_animal}</p>
                  <p><strong>Raza:</strong> {selectedAnimal.raza}</p>
                  <p><strong>Edad:</strong> {selectedAnimal.edad} años</p>
                  <p><strong>Peso:</strong> {selectedAnimal.peso_kg} kg</p>
                  <p><strong>Sexo:</strong> {selectedAnimal.sexo === 'M' ? 'Macho' : 'Hembra'}</p>
                  <p><strong>Color:</strong> {selectedAnimal.color}</p>
                  {selectedAnimal.geocerca_nombre && (
                    <p><strong>Geocerca Asignada:</strong> {selectedAnimal.geocerca_nombre}</p>
                  )}
                  <hr />
                  <h4>Telemetría Actual</h4>
                  <p><strong>Temperatura:</strong> {selectedAnimal.temperatura_corporal ? `${selectedAnimal.temperatura_corporal}°C` : 'N/A'}</p>
                  <p><strong>Frecuencia Cardíaca:</strong> {selectedAnimal.frecuencia_cardiaca ? `${selectedAnimal.frecuencia_cardiaca} lpm` : 'N/A'}</p>
                  <p><strong>Ubicación:</strong> {selectedAnimal.latitud ? `${selectedAnimal.latitud.toFixed(4)}, ${selectedAnimal.longitud.toFixed(4)}` : 'N/A'}</p>
                </div>
              </div>
            )}
          </>
        ) : (
          <div className="alertas-view">
            <AlertasManager />
          </div>
        )}
      </div>
    </div>
  );
};

export default UserDashboard;
