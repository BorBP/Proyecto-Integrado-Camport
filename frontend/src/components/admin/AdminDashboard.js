import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import UserTable from './UserTable';
import AnimalTable from './AnimalTable';
import GeofenceEditor from './GeofenceEditor';
import './AdminDashboard.css';

const AdminDashboard = () => {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('users');
  const navigate = useNavigate();

  return (
    <div className="admin-container">
      <div className="admin-header">
        <h1>⚙️ Panel de Administración</h1>
        <div className="header-actions">
          <button onClick={() => navigate('/')} className="btn-dashboard">
            Dashboard
          </button>
          <span className="user-info">👤 {user?.username}</span>
          <button onClick={logout} className="btn-logout">Cerrar Sesión</button>
        </div>
      </div>

      <div className="admin-content">
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'users' ? 'active' : ''}`}
            onClick={() => setActiveTab('users')}
          >
            👥 Usuarios
          </button>
          <button
            className={`tab ${activeTab === 'animals' ? 'active' : ''}`}
            onClick={() => setActiveTab('animals')}
          >
            🐄 Ganado
          </button>
          <button
            className={`tab ${activeTab === 'geofence' ? 'active' : ''}`}
            onClick={() => setActiveTab('geofence')}
          >
            🗺️ Geocerca
          </button>
        </div>

        <div className="tab-content">
          {activeTab === 'users' && <UserTable />}
          {activeTab === 'animals' && <AnimalTable />}
          {activeTab === 'geofence' && <GeofenceEditor />}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
