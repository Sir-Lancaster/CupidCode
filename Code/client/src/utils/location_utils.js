
import { makeRequest } from './make_request.js';
/**
 * Calculate distance between two coordinates using Haversine formula
 * @param {number} lat1 - Latitude of first point
 * @param {number} lon1 - Longitude of first point  
 * @param {number} lat2 - Latitude of second point
 * @param {number} lon2 - Longitude of second point
 * @returns {number} Distance in miles
 */
export function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 3959; // Earth's radius in miles
  const dLat = toRadians(lat2 - lat1);
  const dLon = toRadians(lon2 - lon1);
  const a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(toRadians(lat1)) * Math.cos(toRadians(lat2)) * 
    Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}

function toRadians(degrees) {
  return degrees * (Math.PI/180);
}

/**
 * Get current location using browser geolocation
 * @returns {Promise<{lat: number, lng: number}>}
 */
export function getCurrentLocation() {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Geolocation not supported'));
      return;
    }
    
    navigator.geolocation.getCurrentPosition(
      position => resolve({
        lat: position.coords.latitude,
        lng: position.coords.longitude
      }),
      error => reject(error),
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 300000 }
    );
  });
}

/**
 * Geocode address to coordinates using Google Maps API
 * @param {string} address - Address to geocode
 * @returns {Promise<{lat: number, lng: number}>}
 */
export async function geocodeAddress(address) {
  await ensureGoogleMapsLoaded(); // Ensure Maps is loaded first
  
  return new Promise((resolve, reject) => {
    const geocoder = new window.google.maps.Geocoder();
    geocoder.geocode({ address }, (results, status) => {
      if (status === 'OK' && results[0]) {
        const location = results[0].geometry.location;
        resolve({ lat: location.lat(), lng: location.lng() });
      } else {
        reject(new Error(`Geocoding failed: ${status}`));
      }
    });
  });
}

/**
 * Filter gigs based on distance from current location to dropoff location
 * @param {Array} gigs - Array of gig objects
 * @param {Object} currentLocation - {lat, lng} of current location
 * @param {number} maxRange - Maximum range in miles (default 10)
 * @returns {Promise<Array>} Filtered array of gigs
 */
export async function filterGigsByRange(gigs, currentLocation, maxRange = 10) {
  if (!currentLocation || !Array.isArray(gigs)) {
    return gigs;
  }

  const filteredGigs = [];
  
  for (const gig of gigs) {
    try {
      // Use pickup location for distance calculation
      const pickupLocation = gig.quest?.pickup_location;
      if (!pickupLocation) {
        // If no pickup location, include the gig
        console.log(`Gig ${gig.id}: No pickup location - including`);
        filteredGigs.push(gig);
        continue;
      }
      const pickupCoords = await geocodeAddress(pickupLocation);
      const distance = calculateDistance(
        currentLocation.lat,
        currentLocation.lng,
        pickupCoords.lat,
        pickupCoords.lng
      );
      console.log(`Gig ${gig.id}: Distance ${distance.toFixed(2)} miles to pickup "${pickupLocation}" - ${distance <= maxRange ? 'INCLUDED' : 'EXCLUDED'}`);
      
      if (distance <= maxRange) {
        filteredGigs.push(gig);
      }
    } catch (error) {
      console.warn('Could not determine location for gig:', gig.id, error);
      // Include gig if we can't determine location
      filteredGigs.push(gig);
    }
  }
  return filteredGigs;
}



async function ensureGoogleMapsLoaded() {
  if (window.google?.maps) {
    return; // Already loaded
  }
  
  try {
    // Fetch API key from backend
    const response = await makeRequest('/api/google-maps-config/');
    const apiKey = response.GOOGLE_MAPS_API_KEY;
    
    if (!apiKey) {
      throw new Error('Google Maps API key not configured');
    }
    
    // Load Google Maps script
    await new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=geometry,places,marker&loading=async`;
      script.async = true;
      script.defer = true;
      
      script.onload = () => {
        if (window.google?.maps) {
          resolve();
        } else {
          reject(new Error('Google Maps failed to load properly'));
        }
      };
      
      script.onerror = () => reject(new Error('Failed to load Google Maps script'));
      document.head.appendChild(script);
    });
  } catch (error) {
    throw new Error(`Failed to load Google Maps: ${error.message}`);
  }
}