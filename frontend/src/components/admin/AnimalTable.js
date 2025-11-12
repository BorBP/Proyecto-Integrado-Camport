import React, { useState, useEffect } from 'react';
import { animalService, geocercaService } from '../../services/api';
import './Tables.css';

const AnimalTable = () => {
  const [animales, setAnimales] = useState([]);
  const [geocercas, setGeocercas] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [formData, setFormData] = useState({
    collar_id: '',
    tipo_animal: 'OVINO',
    raza: '',
    edad: '',
    peso_kg: '',
    sexo: 'M',
    color: '',
    geocerca: ''
  });

  useEffect(() => {
    loadAnimales();
    loadGeocercas();
  }, []);

  const loadAnimales = async () => {
    try {
      const data = await animalService.getAll();
      setAnimales(data);
    } catch (error) {
      console.error('Error loading animals:', error);
    }
  };

  const loadGeocercas = async () => {
    try {
      const data = await geocercaService.getAll();
      setGeocercas(data);
    } catch (error) {
      console.error('Error loading geocercas:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editing) {
        await animalService.update(editing, formData);
      } else {
        await animalService.create(formData);
      }
      loadAnimales();
      resetForm();
    } catch (error) {
      console.error('Error saving animal:', error);
      alert('Error al guardar animal');
    }
  };

  const handleEdit = (animal) => {
    setEditing(animal.collar_id);
    setFormData(animal);
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar este animal?')) {
      try {
        await animalService.delete(id);
        loadAnimales();
      } catch (error) {
        console.error('Error deleting animal:', error);
      }
    }
  };

  const resetForm = () => {
    setShowForm(false);
    setEditing(null);
    setFormData({
      collar_id: '',
      tipo_animal: 'OVINO',
      raza: '',
      edad: '',
      peso_kg: '',
      sexo: 'M',
      color: '',
      geocerca: ''
    });
  };

  return (
    <div className="table-container">
      <div className="table-header">
        <h2>Gestión de Ganado</h2>
        <button onClick={() => setShowForm(!showForm)} className="btn-add">
          {showForm ? 'Cancelar' : '+ Nuevo Animal'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="form-card">
          <div className="form-row">
            <div className="form-group">
              <label>ID del Collar*</label>
              <input
                type="text"
                value={formData.collar_id}
                onChange={(e) => setFormData({...formData, collar_id: e.target.value})}
                required
                disabled={editing}
              />
            </div>
            <div className="form-group">
              <label>Tipo de Animal*</label>
              <select
                value={formData.tipo_animal}
                onChange={(e) => setFormData({...formData, tipo_animal: e.target.value})}
                required
              >
                <option value="OVINO">Ovino</option>
                <option value="BOVINO">Bovino</option>
                <option value="EQUINO">Equino</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Raza*</label>
              <input
                type="text"
                value={formData.raza}
                onChange={(e) => setFormData({...formData, raza: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Edad (años)*</label>
              <input
                type="number"
                value={formData.edad}
                onChange={(e) => setFormData({...formData, edad: e.target.value})}
                required
                min="0"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Peso (kg)*</label>
              <input
                type="number"
                step="0.1"
                value={formData.peso_kg}
                onChange={(e) => setFormData({...formData, peso_kg: e.target.value})}
                required
                min="0"
              />
            </div>
            <div className="form-group">
              <label>Sexo*</label>
              <select
                value={formData.sexo}
                onChange={(e) => setFormData({...formData, sexo: e.target.value})}
                required
              >
                <option value="M">Macho</option>
                <option value="H">Hembra</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Color*</label>
              <input
                type="text"
                value={formData.color}
                onChange={(e) => setFormData({...formData, color: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Geocerca Asignada</label>
              <select
                value={formData.geocerca}
                onChange={(e) => setFormData({...formData, geocerca: e.target.value})}
              >
                <option value="">Sin geocerca</option>
                {geocercas.map(g => (
                  <option key={g.id} value={g.id}>
                    {g.nombre} ({g.animales_count || 0} animales)
                  </option>
                ))}
              </select>
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
            <th>ID Display</th>
            <th>Collar ID</th>
            <th>Tipo</th>
            <th>Raza</th>
            <th>Edad</th>
            <th>Peso</th>
            <th>Sexo</th>
            <th>Geocerca</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {animales.map(animal => (
            <tr key={animal.collar_id}>
              <td><strong>{animal.display_id || '-'}</strong></td>
              <td>{animal.collar_id}</td>
              <td>
                <span className={`badge badge-${animal.tipo_animal.toLowerCase()}`}>
                  {animal.tipo_animal}
                </span>
              </td>
              <td>{animal.raza}</td>
              <td>{animal.edad} años</td>
              <td>{animal.peso_kg} kg</td>
              <td>{animal.sexo === 'M' ? 'Macho' : 'Hembra'}</td>
              <td>{animal.geocerca_nombre || 'Sin asignar'}</td>
              <td>
                <button onClick={() => handleEdit(animal)} className="btn-edit">
                  ✏️
                </button>
                <button onClick={() => handleDelete(animal.collar_id)} className="btn-delete">
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

export default AnimalTable;
