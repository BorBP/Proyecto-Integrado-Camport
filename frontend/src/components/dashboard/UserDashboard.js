import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import useWebSocket from '../../hooks/useWebSocket';
import { animalService, geocercaService } from '../../services/api';
import MapComponent from '../map/MapContainer';
import NotificationBell from './NotificationBell';
import './UserDashboard.css';

const UserDashboard = () => {
  const { user, logout } = useAuth();
  const [animales, setAnimales] = useState([]);
  const [geocerca, setGeocerca] = useState(null);
  const [selectedAnimal, setSelectedAnimal] = useState(null);
  
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
      const [animalesData, geocercaData] = await Promise.all([
        animalService.getAll(),
        geocercaService.getActiva().catch(() => null)
      ]);
      
      setAnimales(animalesData);
      setGeocerca(geocercaData);
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  const updateAnimalData = (telemetriaData) => {
    setAnimales(prevAnimales => 
      prevAnimales.map(animal => 
        animal.collar_id === telemetriaData.collar_id
          ? {
              ...animal,
              latitud: telemetriaData.latitud,
              longitud: telemetriaData.longitud,
              temperatura_corporal: telemetriaData.temperatura_corporal,
              frecuencia_cardiaca: telemetriaData.frecuencia_cardiaca,
            }
          : animal
      )
    );
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>🐄 Monitor de Ganado en Tiempo Real</h1>
        <div className="header-actions">
          <div className="connection-status">
            <span className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}></span>
            {isConnected ? 'Conectado' : 'Desconectado'}
          </div>
          <NotificationBell />
          <div className="user-info">
            <span>👤 {user?.username}</span>
            {user?.is_staff && <span className="admin-badge">Admin</span>}
          </div>
          <button onClick={logout} className="btn-logout">Cerrar Sesión</button>
        </div>
      </div>

      <div className="dashboard-content">
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
                  <strong>{animal.collar_id}</strong>
                  <p>{animal.tipo_animal} - {animal.raza}</p>
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
            geocerca={geocerca}
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
              <h4>{selectedAnimal.collar_id}</h4>
              <p><strong>Tipo:</strong> {selectedAnimal.tipo_animal}</p>
              <p><strong>Raza:</strong> {selectedAnimal.raza}</p>
              <p><strong>Edad:</strong> {selectedAnimal.edad} años</p>
              <p><strong>Peso:</strong> {selectedAnimal.peso_kg} kg</p>
              <p><strong>Sexo:</strong> {selectedAnimal.sexo === 'M' ? 'Macho' : 'Hembra'}</p>
              <p><strong>Color:</strong> {selectedAnimal.color}</p>
              <hr />
              <h4>Telemetría Actual</h4>
              <p><strong>Temperatura:</strong> {selectedAnimal.temperatura_corporal ? `${selectedAnimal.temperatura_corporal}°C` : 'N/A'}</p>
              <p><strong>Frecuencia Cardíaca:</strong> {selectedAnimal.frecuencia_cardiaca ? `${selectedAnimal.frecuencia_cardiaca} lpm` : 'N/A'}</p>
              <p><strong>Ubicación:</strong> {selectedAnimal.latitud ? `${selectedAnimal.latitud.toFixed(4)}, ${selectedAnimal.longitud.toFixed(4)}` : 'N/A'}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default UserDashboard;
