import React from 'react';
import { Marker, Popup } from 'react-leaflet';
import L from 'leaflet';

const AnimalMarker = ({ animal, onClick }) => {
  // Determinar el emoji según el tipo de animal
  const getAnimalEmoji = (tipo) => {
    switch(tipo) {
      case 'OVINO':
        return '🐑';
      case 'BOVINO':
        return '🐄';
      case 'EQUINO':
        return '🐎';
      default:
        return '📍';
    }
  };

  // Crear icono personalizado con emoji
  const customIcon = L.divIcon({
    html: `<div style="font-size: 30px; text-align: center;">${getAnimalEmoji(animal.tipo_animal)}</div>`,
    className: 'animal-marker',
    iconSize: [40, 40],
    iconAnchor: [20, 20],
  });

  const position = [animal.latitud || -38.8444, animal.longitud || -72.2946];

  return (
    <Marker position={position} icon={customIcon} eventHandlers={{ click: onClick }}>
      <Popup>
        <div style={{ minWidth: '200px' }}>
          <h3>{animal.collar_id}</h3>
          <p><strong>Tipo:</strong> {animal.tipo_animal}</p>
          <p><strong>Raza:</strong> {animal.raza}</p>
          <p><strong>Temperatura:</strong> {animal.temperatura_corporal ? `${animal.temperatura_corporal}°C` : 'N/A'}</p>
          <p><strong>Frecuencia Cardíaca:</strong> {animal.frecuencia_cardiaca ? `${animal.frecuencia_cardiaca} lpm` : 'N/A'}</p>
          <p><strong>Ubicación:</strong> {position[0].toFixed(4)}, {position[1].toFixed(4)}</p>
        </div>
      </Popup>
    </Marker>
  );
};

export default AnimalMarker;
