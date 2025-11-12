import React from 'react';
import { Polygon, Tooltip } from 'react-leaflet';

const GeofenceLayer = ({ coordenadas, nombre }) => {
  if (!coordenadas || coordenadas.length === 0) return null;

  // Convertir coordenadas al formato que espera Leaflet [lat, lng]
  const positions = coordenadas.map(coord => [coord.lat, coord.lng]);

  // Colores diferentes para diferentes geocercas
  const colors = ['blue', 'green', 'purple', 'orange', 'red'];
  const colorIndex = nombre ? nombre.charCodeAt(0) % colors.length : 0;
  const color = colors[colorIndex];

  return (
    <Polygon
      positions={positions}
      pathOptions={{
        color: color,
        fillColor: color,
        fillOpacity: 0.2,
        weight: 2,
      }}
    >
      {nombre && <Tooltip permanent>{nombre}</Tooltip>}
    </Polygon>
  );
};

export default GeofenceLayer;
