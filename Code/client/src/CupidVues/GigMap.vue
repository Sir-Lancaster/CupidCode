<script setup>
import { ref, onMounted } from 'vue'
import { makeRequest } from '../utils/make_request.js'

const props = defineProps({
  pickupLocation: {
    type: String,
    default: '40.12150192260742,-100.45039367675781'
  },
  dropoffLocation: {
    type: String,
    default: null
  },
  gigTitle: {
    type: String,
    default: 'Gig Location'
  }
})

const emit = defineEmits(['close'])

const isLoading = ref(true)
const errorMessage = ref('')
const currentLocation = ref(null)
const pickupCoords = ref(null)
const dropoffCoords = ref(null)
const routeInfo = ref({
  toPickupDuration: '',
  toDropoffDuration: '',
  totalDurationText: '',
  totalDistanceText: ''
})

// Parse coordinates or return null for addresses
function parseCoordinates(locationString) {
  if (!locationString) return null
  
  const coordsPattern = /^[-\d\s.,]+$/
  if (!coordsPattern.test(locationString)) return null
  
  const coords = locationString.split(',')
  if (coords.length >= 2) {
    const lat = parseFloat(coords[0].trim())
    const lng = parseFloat(coords[1].trim())
    
    if (!isNaN(lat) && !isNaN(lng) && lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180) {
      return { lat, lng }
    }
  }
  return null
}

// Geocode address to coordinates
function geocodeAddress(address) {
  return new Promise((resolve, reject) => {
    if (!window.google?.maps) {
      reject(new Error('Google Maps not loaded'))
      return
    }
    
    const geocoder = new window.google.maps.Geocoder()
    geocoder.geocode({ address }, (results, status) => {
      if (status === 'OK' && results[0]) {
        const location = results[0].geometry.location
        resolve({ lat: location.lat(), lng: location.lng() })
      } else {
        reject(new Error(`Geocoding failed: ${status}`))
      }
    })
  })
}

// Helper to read CSS variables at runtime
function cssVar(name, fallback = '') {
  try {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim() || fallback
  } catch (e) {
    return fallback
  }
}

// Create route between two points with specific color
async function createRoute(map, origin, destination, color, suppressMarkers = true) {
  const directionsService = new window.google.maps.DirectionsService()
  const directionsRenderer = new window.google.maps.DirectionsRenderer({
    suppressMarkers,
    polylineOptions: {
      strokeColor: color,
      strokeOpacity: 0.8,
      strokeWeight: 4
    }
  })
  
  directionsRenderer.setMap(map)
  
  return new Promise((resolve, reject) => {
    directionsService.route({
      origin,
      destination,
      travelMode: window.google.maps.TravelMode.DRIVING
    }, (result, status) => {
      if (status === 'OK') {
        directionsRenderer.setDirections(result)
        resolve(result)
      } else {
        reject(new Error(`Directions failed: ${status}`))
      }
    })
  })
}

// Add this function at the top of the script section
async function getCurrentLocation() {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      console.warn('Geolocation not supported')
      // Use Salt Lake City as fallback
      resolve({ lat: 40.7589, lng: -111.8883 })
      return
    }

    console.log('Requesting geolocation permission...')
    
    navigator.geolocation.getCurrentPosition(
      (position) => {
        console.log('Got user location:', position.coords)
        resolve({
          lat: position.coords.latitude,
          lng: position.coords.longitude
        })
      },
      (error) => {
        console.warn('Geolocation error:', error.message)
        
        // Handle different error types
        switch(error.code) {
          case error.PERMISSION_DENIED:
            console.warn('Location access denied by user')
            break
          case error.POSITION_UNAVAILABLE:
            console.warn('Location information unavailable')
            break
          case error.TIMEOUT:
            console.warn('Location request timed out')
            break
        }
        
        // Always resolve with fallback location instead of rejecting
        resolve({ lat: 40.7589, lng: -111.8883 })
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 300000 // 5 minutes
      }
    )
  })
}

// Main map initialization
async function initializeMap() {
  try {
    console.log('Initializing map...')
    
    // Verify Google Maps is loaded
    if (!window.google?.maps?.Map) {
      throw new Error('Google Maps not properly loaded')
    }

    // Get current location with explicit permission request
    console.log('Getting current location...')
    currentLocation.value = await getCurrentLocation()
    console.log('Current location:', currentLocation.value)

    // Parse pickup location
    pickupCoords.value = parseCoordinates(props.pickupLocation)
    if (!pickupCoords.value && props.pickupLocation) {
      try {
        pickupCoords.value = await geocodeAddress(props.pickupLocation)
      } catch (error) {
        console.warn('Could not geocode pickup:', error)
      }
    }

    // Parse dropoff location
    if (props.dropoffLocation) {
      dropoffCoords.value = parseCoordinates(props.dropoffLocation)
      if (!dropoffCoords.value) {
        try {
          dropoffCoords.value = await geocodeAddress(props.dropoffLocation)
        } catch (error) {
          console.warn('Could not geocode dropoff:', error)
        }
      }
    }

    // Set map center
    const center = pickupCoords.value || currentLocation.value || { lat: 40.7589, lng: -111.8883 }
    console.log('Map center:', center)

    // Create map with Map ID to support Advanced Markers
    const mapElement = document.getElementById('gig-map')
    if (!mapElement) {
      throw new Error('Map container element not found')
    }

    console.log('Creating Google Map...')
    const map = new window.google.maps.Map(mapElement, {
      center,
      zoom: 13,
      mapId: 'cupid-gig-map' // Add Map ID for Advanced Markers
    })

    console.log('Map created successfully')
    
    // Add markers using AdvancedMarkerElement with updated properties
    if (currentLocation.value) {
      // Create custom pin element for current location
        const currentLocationPin = new google.maps.marker.PinElement({
          background: cssVar('--new-light-blue', '#00CCFF'),
          borderColor: cssVar('--on-button-text', '#ffffff'),
          glyphColor: cssVar('--on-button-text', '#ffffff'),
          glyphText: '📍', // Use glyphText instead of glyph
          scale: 1.2
        })
      
      new google.maps.marker.AdvancedMarkerElement({
        position: currentLocation.value,
        map,
        title: 'Your Location',
        content: currentLocationPin.element
      })
    }
    
    if (pickupCoords.value) {
      // Create custom pin element for pickup location
      const pickupPin = new google.maps.marker.PinElement({
        background: cssVar('--new-primary', '#09A129'),
        borderColor: cssVar('--on-button-text', '#ffffff'),
        glyphColor: cssVar('--on-button-text', '#ffffff'),
        glyphText: '🏠', // Use glyphText instead of glyph
        scale: 1.2
      })
      
      new google.maps.marker.AdvancedMarkerElement({
        position: pickupCoords.value,
        map,
        title: 'Pickup Location',
        content: pickupPin.element
      })
    }
    
    if (dropoffCoords.value) {
      // Create custom pin element for dropoff location
      const dropoffPin = new google.maps.marker.PinElement({
        background: cssVar('--new-accent', '#FB3640'),
        borderColor: cssVar('--on-button-text', '#ffffff'),
        glyphColor: cssVar('--on-button-text', '#ffffff'),
        glyphText: '🎯', // Use glyphText instead of glyph
        scale: 1.2
      })
      
      new google.maps.marker.AdvancedMarkerElement({
        position: dropoffCoords.value,
        map,
        title: 'Dropoff Location',
        content: dropoffPin.element
      })
    }
    
    // Create routes with different colors
    if (currentLocation.value && pickupCoords.value) {
      try {
  // Route: Current location to pickup (uses theme accent for visibility)
  const toPickupRoute = await createRoute(map, currentLocation.value, pickupCoords.value, cssVar('--new-light-blue', '#FFD700'))
        const toPickupLeg = toPickupRoute.routes[0].legs[0]
        routeInfo.value.toPickupDuration = toPickupLeg.duration.text
        
        if (dropoffCoords.value) {
          // Route: Pickup to dropoff
          const toDropoffRoute = await createRoute(map, pickupCoords.value, dropoffCoords.value, cssVar('--new-accent', '#FB3640'))
          const toDropoffLeg = toDropoffRoute.routes[0].legs[0]
          routeInfo.value.toDropoffDuration = toDropoffLeg.duration.text
          
          // Calculate totals
          const totalDuration = toPickupLeg.duration.value + toDropoffLeg.duration.value
          const totalDistance = toPickupLeg.distance.value + toDropoffLeg.distance.value
          
          const totalMinutes = Math.round(totalDuration / 60)
          const hours = Math.floor(totalMinutes / 60)
          const minutes = totalMinutes % 60
          
          routeInfo.value.totalDurationText = hours > 0 ? `${hours}h ${minutes}m` : `${minutes}m`
          routeInfo.value.totalDistanceText = `${(totalDistance * 0.000621371).toFixed(1)} mi`
        } else {
          routeInfo.value.totalDurationText = toPickupLeg.duration.text
          routeInfo.value.totalDistanceText = toPickupLeg.distance.text
        }
        
        // Fit map to show all points
        const bounds = new window.google.maps.LatLngBounds()
        if (currentLocation.value) bounds.extend(currentLocation.value)
        if (pickupCoords.value) bounds.extend(pickupCoords.value)
        if (dropoffCoords.value) bounds.extend(dropoffCoords.value)
        map.fitBounds(bounds)
        
      } catch (error) {
        console.warn('Could not create routes:', error)
      }
    }
    
  } catch (error) {
    console.error('Map initialization error:', error)
    errorMessage.value = `Map error: ${error.message}`
  } finally {
    isLoading.value = false
  }
}

// Load Google Maps script with proper async loading
// Load Google Maps script with proper async loading
function loadGoogleMapsScript(apiKey) {
  return new Promise((resolve, reject) => {
    // Check if Google Maps is already loaded
    if (window.google && window.google.maps && window.google.maps.Map) {
      resolve()
      return
    }

    // Check if script is already loading
    if (document.querySelector('script[src*="maps.googleapis.com"]')) {
      // Wait for existing script to load
      const checkLoaded = setInterval(() => {
        if (window.google && window.google.maps && window.google.maps.Map) {
          clearInterval(checkLoaded)
          resolve()
        }
      }, 100)
      
      setTimeout(() => {
        clearInterval(checkLoaded)
        reject(new Error('Google Maps loading timeout'))
      }, 10000)
      return
    }

    const script = document.createElement('script')
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=geometry,places,marker&loading=async`
    script.async = true
    script.defer = true
    
    script.onload = () => {
      // Wait for Google Maps to be fully loaded with a timeout
      const checkGoogle = () => {
        if (window.google && window.google.maps && window.google.maps.Map) {
          resolve()
        } else {
          setTimeout(checkGoogle, 50)
        }
      }
      checkGoogle()
    }
    
    script.onerror = () => {
      reject(new Error('Failed to load Google Maps script'))
    }
    
    document.head.appendChild(script)
    
    // Fallback timeout
    setTimeout(() => {
      reject(new Error('Google Maps loading timeout'))
    }, 10000)
  })
}

// Load Google Maps and initialize
onMounted(async () => {
  try {
    console.log('Starting map initialization...')
    
    // Get Google Maps config
    const config = await makeRequest('/api/google-maps-config/')
    if (!config?.GOOGLE_MAPS_API_KEY) {
      throw new Error('Google Maps API key not configured')
    }

    console.log('Loading Google Maps script...')
    
    // Load Google Maps with proper waiting
    await loadGoogleMapsScript(config.GOOGLE_MAPS_API_KEY)
    
    console.log('Google Maps loaded, initializing map...')
    
    // Initialize map
    await initializeMap()
    
  } catch (error) {
    console.error('Failed to load map:', error)
    errorMessage.value = `Failed to load map: ${error.message}`
    isLoading.value = false
  }
})

function closeMap() {
  emit('close')
}
</script>

<!-- Template and styles remain the same -->
<template>
  <div class="map-overlay">
    <div class="map-container">
      <div class="map-header">
        <h2>{{ gigTitle }}</h2>
        <button @click="closeMap" class="close-btn">&times;</button>
      </div>
      <div class="map-content">
        <!-- Loading State -->
        <div v-if="isLoading" class="loading-overlay">
          <div class="loading-spinner"></div>
          <p>Loading map...</p>
        </div>
        
        <!-- Error State -->
        <div v-if="errorMessage && !isLoading" class="error-overlay">
          <p>{{ errorMessage }}</p>
        </div>
        
        <div id="gig-map" style="width: 100%; height: 100%;"></div>
        
        <!-- Map Legend -->
        <div class="map-legend" v-if="!isLoading">
          <h4>Map Legend</h4>
          <div class="legend-item" v-if="currentLocation">
            <div class="legend-marker current">📍</div>
            <span>Your Location</span>
          </div>
          <div class="legend-item" v-if="pickupCoords">
            <div class="legend-marker pickup">🏠</div>
            <span>Pickup</span>
          </div>
          <div class="legend-item" v-if="dropoffCoords">
            <div class="legend-marker dropoff">🎯</div>
            <span>Dropoff</span>
          </div>
          <div class="legend-item">
            <div class="legend-path yellow"></div>
            <span>To Pickup</span>
          </div>
          <div class="legend-item" v-if="dropoffCoords">
            <div class="legend-path red"></div>
            <span>To Dropoff</span>
          </div>
        </div>
        
        <!-- Route Information -->
        <div class="route-info" v-if="!isLoading && routeInfo.totalDurationText">
          <h4>Route Info</h4>
          <div class="route-item" v-if="routeInfo.toPickupDuration">
            <span class="route-label">To Pickup:</span>
            <span class="route-value">{{ routeInfo.toPickupDuration }}</span>
          </div>
          <div class="route-item" v-if="routeInfo.toDropoffDuration">
            <span class="route-label">To Dropoff:</span>
            <span class="route-value">{{ routeInfo.toDropoffDuration }}</span>
          </div>
          <div class="route-item total">
            <span class="route-label">Total:</span>
            <span class="route-value">{{ routeInfo.totalDurationText }}</span>
          </div>
          <div class="route-item" v-if="routeInfo.totalDistanceText">
            <span class="route-label">Distance:</span>
            <span class="route-value">{{ routeInfo.totalDistanceText }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.map-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  padding: 20px;
  box-sizing: border-box;
}

.map-container {
  background-color: var(--new-background);
  border: 2px solid var(--new-primary);
  border-radius: 8px;
  width: 90%;
  max-width: 1600px;
  height: 80%;
  max-height: 1200px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.map-header {
  background-color: var(--new-secondary);
  color: var(--new-primary);
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #09A129;
}

.map-header h2 {
  margin: 0;
  font-size: 1.4em;
}

.close-btn {
  background: none;
  border: none;
  color: var(--new-primary);
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background-color: var(--new-primary);
  color: var(--new-background);
}

.map-content {
  flex: 1;
  position: relative;
  overflow: hidden;
}

#gig-map {
  width: 100%;
  height: 100%;
}

.map-legend {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: rgba(0, 0, 0, 0.6);
  border: 1px solid var(--new-primary);
  border-radius: 4px;
  padding: 10px;
  color: var(--new-primary);
  min-width: 140px;
}

.map-legend h4 {
  margin: 0 0 8px 0;
  font-size: 0.9em;
  color: #09A129;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-bottom: 4px;
  font-size: 0.8em;
}

.legend-marker {
  margin-right: 8px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8em;
}

.legend-marker.current {
  background: var(--new-light-blue);
}

.legend-marker.pickup {
  background: var(--new-primary);
}

.legend-marker.dropoff {
  background: var(--new-accent);
}

.legend-path {
  margin-right: 8px;
  width: 20px;
  height: 4px;
  border-radius: 2px;
}

.legend-path.yellow {
  background: var(--new-light-blue);
}

.legend-path.red {
  background: var(--new-accent);
}

.route-info {
  position: absolute;
  bottom: 10px;
  left: 10px;
  background-color: rgba(0, 0, 0, 0.6);
  border: 1px solid var(--new-primary);
  border-radius: 4px;
  padding: 10px;
  color: var(--new-primary);
  min-width: 160px;
}

.route-info h4 {
  margin: 0 0 8px 0;
  font-size: 0.9em;
  color: #09A129;
}

.route-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
  font-size: 0.8em;
}

.route-item.total {
  border-top: 1px solid var(--new-primary);
  padding-top: 4px;
  margin-top: 4px;
  font-weight: bold;
}
.route-label {
  color: var(--new-primary);
}

.route-value {
  color: var(--new-light-blue);
  font-weight: bold;
}

.loading-overlay, .error-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--new-primary);
  z-index: 1000;
}

.loading-spinner {
  border: 3px solid rgba(9, 161, 41, 0.3);
  border-top: 3px solid var(--new-primary);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-overlay p {
  text-align: center;
  margin: 0;
  padding: 20px;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .map-overlay {
    padding: 10px;
  }
  
  .map-container {
    width: 95%;
    height: 85%;
  }
  
  .map-header {
    padding: 12px 15px;
  }
  
  .map-header h2 {
    font-size: 1.2em;
  }
  
  .map-legend {
    right: 5px;
    top: 5px;
    min-width: 120px;
    font-size: 0.7em;
  }
  
  .route-info {
    left: 5px;
    bottom: 5px;
    min-width: 140px;
    font-size: 0.7em;
  }
  
  .route-item {
    font-size: 0.7em;
  }
}
</style>