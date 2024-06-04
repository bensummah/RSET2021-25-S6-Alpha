// src/IndoorMap.js

import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-routing-machine';
import { userLocations, destinations } from './coordinates';

const IndoorMap = ({ userLocationKey, destinationKey }) => {
  const mapRef = useRef(null);

  useEffect(() => {
    // Initialize the map only if it hasn't been initialized yet
    if (mapRef.current) return;

    // Define the dimensions and coordinates for the map overlay
    const mapBounds = [[0, 0], [1000, 1000]]; // adjust based on your image dimensions

    // Initialize the map
    const map = L.map('map', {
      crs: L.CRS.Simple,
      minZoom: -1,
      maxZoom: 4,
    }).setView([500, 500], 0);

    // Store the map instance in the ref
    mapRef.current = map;

    // Load the floor plan image
    L.imageOverlay('/floorplan.png', mapBounds).addTo(map);

    // Clean up the map instance on unmount
    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, []);

  useEffect(() => {
    if (!mapRef.current) return;

    const map = mapRef.current;

    // Remove any existing layers (e.g., previous paths and markers)
    map.eachLayer(layer => {
      if (layer instanceof L.Marker || layer instanceof L.Polyline) {
        map.removeLayer(layer);
      }
    });

    // Get the user location and destination coordinates from the keys
    const userLocation = userLocations[userLocationKey];
    const destination = destinations[destinationKey];
    if (!userLocation || !destination) return;

    // Add a marker for the user's current location
    const userMarker = L.marker(userLocation).addTo(map);
    userMarker.bindPopup('Your location').openPopup();

    // Add a marker for the destination
    const destMarker = L.marker(destination).addTo(map);
    destMarker.bindPopup('Destination').openPopup();

    // Use a simple line for the path
    const pathCoordinates = [userLocation, destination];
    const path = L.polyline(pathCoordinates, { color: 'blue' }).addTo(map);

    // Optionally, add an arrow marker at the start of the path
    const arrow = L.marker(userLocation, {
      icon: L.divIcon({
        className: 'custom-arrow',
        html: '<div style="transform: rotate(45deg);">&#10148;</div>',
        iconSize: [24, 24],
      }),
    }).addTo(map);
  }, [userLocationKey, destinationKey]);

  return <div id="map" style={{ height: '500px', width: '100%' }} />;
};

export default IndoorMap;