import React, { useState, useEffect } from 'react';
import { userService } from '../../services/api';
import './Tables.css';

const UserTable = () => {
  const [users, setUsers] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    RUT: '',
    domicilio: '',
    sexo: 'M',
    fecha_nacimiento: '',
    is_staff: false,
    password: ''
  });

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      const data = await userService.getAll();
      setUsers(data);
    } catch (error) {
      console.error('Error loading users:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editing) {
        await userService.update(editing, formData);
      } else {
        await userService.create(formData);
      }
      loadUsers();
      resetForm();
    } catch (error) {
      console.error('Error saving user:', error);
      alert('Error al guardar usuario');
    }
  };

  const handleEdit = (user) => {
    setEditing(user.id);
    setFormData({ ...user, password: '' });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar este usuario?')) {
      try {
        await userService.delete(id);
        loadUsers();
      } catch (error) {
        console.error('Error deleting user:', error);
      }
    }
  };

  const resetForm = () => {
    setShowForm(false);
    setEditing(null);
    setFormData({
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      RUT: '',
      domicilio: '',
      sexo: 'M',
      fecha_nacimiento: '',
      is_staff: false,
      password: ''
    });
  };

  return (
    <div className="table-container">
      <div className="table-header">
        <h2>Gestión de Usuarios</h2>
        <button onClick={() => setShowForm(!showForm)} className="btn-add">
          {showForm ? 'Cancelar' : '+ Nuevo Usuario'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="form-card">
          <div className="form-row">
            <div className="form-group">
              <label>Usuario*</label>
              <input
                type="text"
                value={formData.username}
                onChange={(e) => setFormData({...formData, username: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Email*</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Nombre</label>
              <input
                type="text"
                value={formData.first_name}
                onChange={(e) => setFormData({...formData, first_name: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Apellido</label>
              <input
                type="text"
                value={formData.last_name}
                onChange={(e) => setFormData({...formData, last_name: e.target.value})}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>RUT*</label>
              <input
                type="text"
                value={formData.RUT}
                onChange={(e) => setFormData({...formData, RUT: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Fecha de Nacimiento*</label>
              <input
                type="date"
                value={formData.fecha_nacimiento}
                onChange={(e) => setFormData({...formData, fecha_nacimiento: e.target.value})}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Domicilio*</label>
              <input
                type="text"
                value={formData.domicilio}
                onChange={(e) => setFormData({...formData, domicilio: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Sexo*</label>
              <select
                value={formData.sexo}
                onChange={(e) => setFormData({...formData, sexo: e.target.value})}
                required
              >
                <option value="M">Masculino</option>
                <option value="F">Femenino</option>
                <option value="O">Otro</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Contraseña{editing ? '' : '*'}</label>
              <input
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                required={!editing}
              />
            </div>
            <div className="form-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={formData.is_staff}
                  onChange={(e) => setFormData({...formData, is_staff: e.target.checked})}
                />
                Es Administrador
              </label>
            </div>
          </div>

          <div className="form-actions">
            <button type="submit" className="btn-save">
              {editing ? 'Actualizar' : 'Crear'}
            </button>
            <button type="button" onClick={resetForm} className="btn-cancel">
              Cancelar
            </button>
          </div>
        </form>
      )}

      <table className="data-table">
        <thead>
          <tr>
            <th>Usuario</th>
            <th>Email</th>
            <th>Nombre</th>
            <th>RUT</th>
            <th>Rol</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.username}</td>
              <td>{user.email}</td>
              <td>{user.first_name} {user.last_name}</td>
              <td>{user.RUT}</td>
              <td>
                <span className={`badge ${user.is_staff ? 'badge-admin' : 'badge-user'}`}>
                  {user.is_staff ? 'Admin' : 'Usuario'}
                </span>
              </td>
              <td>
                <button onClick={() => handleEdit(user)} className="btn-edit">
                  ✏️
                </button>
                <button onClick={() => handleDelete(user.id)} className="btn-delete">
                  🗑️
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default UserTable;
