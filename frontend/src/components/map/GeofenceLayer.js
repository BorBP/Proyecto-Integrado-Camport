import React from 'react';
import { Polygon } from 'react-leaflet';

const GeofenceLayer = ({ coordenadas }) => {
  if (!coordenadas || coordenadas.length === 0) return null;

  // Convertir coordenadas al formato que espera Leaflet [lat, lng]
  const positions = coordenadas.map(coord => [coord.lat, coord.lng]);

  return (
    <Polygon
      positions={positions}
      pathOptions={{
        color: 'blue',
        fillColor: 'lightblue',
        fillOpacity: 0.2,
        weight: 2,
      }}
    />
  );
};

export default GeofenceLayer;
