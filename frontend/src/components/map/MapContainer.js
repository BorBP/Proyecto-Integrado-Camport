import React from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import AnimalMarker from './AnimalMarker';
import GeofenceLayer from './GeofenceLayer';
import './MapComponent.css';

// Fix para los iconos de Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const MapComponent = ({ animales, geocerca, onAnimalClick }) => {
  const center = [-38.8444, -72.2946]; // Coordenadas de La Araucanía, Chile
  const zoom = 14;

  return (
    <div className="map-container">
      <MapContainer center={center} zoom={zoom} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {geocerca && <GeofenceLayer coordenadas={geocerca.coordenadas} />}
        
        {animales.map((animal) => (
          <AnimalMarker
            key={animal.collar_id}
            animal={animal}
            onClick={() => onAnimalClick(animal)}
          />
        ))}
      </MapContainer>
    </div>
  );
};

export default MapComponent;
