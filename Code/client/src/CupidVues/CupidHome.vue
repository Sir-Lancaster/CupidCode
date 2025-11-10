<script setup>
import {ref, onMounted, computed} from 'vue';
import router from '../router/index.js'
import { makeRequest } from '../utils/make_request';
import { getCurrentLocation, filterGigsByRange } from '../utils/location_utils';

import CupidBanner from './components/CupidBanner.vue';
import CupidNavBar from './components/CupidNavBar.vue';
import GigData from './components/GigData.vue'
import GigMap from './GigMap.vue' 

const user_id  = parseInt(window.location.hash.split('/')[3])
const gigCount = 0
const gigs = ref([])
const activeGigs = ref([])
const reward = ref(0)
const rewardShow = ref(false)
const showMap = ref(false) 
const selectedGig = ref(null) 
const currentLocation = ref(null)
const cupidRange = ref(10) // Default range
const isLoadingLocation = ref(false)

async function getData() {
    try {
        // Get cupid profile first
        const cupidProfile = await makeRequest(`api/user/${user_id}`)
        cupidRange.value = cupidProfile.gig_range || 10
        
        // Load Google Maps API if not already loaded
        if (!window.google?.maps) {
            try {
                const response = await makeRequest('/api/google-maps-config/')
                const apiKey = response.GOOGLE_MAPS_API_KEY
                
                if (apiKey) {
                    await new Promise((resolve, reject) => {
                        const script = document.createElement('script')
                        script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=geometry,places,marker&loading=async`
                        script.async = true
                        script.defer = true
                        
                        script.onload = () => {
                            if (window.google?.maps) {
                                console.log('Google Maps API loaded successfully')
                                resolve()
                            } else {
                                reject(new Error('Google Maps failed to load properly'))
                            }
                        }
                        
                        script.onerror = () => reject(new Error('Failed to load Google Maps script'))
                        document.head.appendChild(script)
                    })
                }
            } catch (error) {
                console.warn('Could not load Google Maps API:', error)
            }
        }
        
        // Get current location
        isLoadingLocation.value = true
        try {
            currentLocation.value = await getCurrentLocation()
        } catch (error) {
            console.warn('Could not get current location:', error)
        }
        isLoadingLocation.value = false
        
        // Get all gigs
        let allGigs = await makeRequest(`api/gig/${user_id}/${gigCount}`)
        let activeGigsResponse = await makeRequest(`api/cupid/gigs/${user_id}?complete=false`)
        
        if (allGigs.detail === 'Not found.'){
            allGigs = []
        }
        if (activeGigsResponse.detail === 'Not found.'){
            activeGigs.value = []
        } else {
            activeGigs.value = activeGigsResponse
        }
        
        // Now filter with Google Maps available
        if (currentLocation.value && Array.isArray(allGigs) && window.google?.maps) {
            gigs.value = await filterGigsByRange(allGigs, currentLocation.value, cupidRange.value)
        } else {
            console.log('Location or Google Maps not available - showing all gigs')
            gigs.value = allGigs
        }
        
    } catch (error) {
        console.error('Error getting data:', error)
        // Fallback to showing all gigs without filtering
        try {
            gigs.value = await makeRequest(`api/gig/${user_id}/${gigCount}`)
            if (gigs.value.detail === 'Not found.') {
                gigs.value = []
            }
        } catch (fallbackError) {
            console.error('Fallback failed:', fallbackError)
            gigs.value = []
        }
    }
}

function displayReward(amount) {
    reward.value = amount
    rewardShow.value = true
    setTimeout(() => {rewardShow.value = false},1500)
}


function openMap(gig) {
    selectedGig.value = gig
    showMap.value = true
}

async function claim(id) {
    try {
        const response = await makeRequest('/api/gig/accept/', 'post', {
           'gig_id': id
        })
            
        if (response.error) {
            alert(response.error)
        } else {
            alert(response.message || 'Gig claimed successfully!')
            getData()
        }
    } catch (error) {
        console.error('Error claiming gig:', error)
        alert('Failed to claim gig. Please try again.')
    }
}


function closeMap() {
    showMap.value = false
    selectedGig.value = null
}

onMounted(getData)
</script>

<template>
    <CupidBanner />
    <CupidNavBar currentPage="CupidHome" />

    <main>
        <h1 class="page-title">Cupid Home</h1>
        
        <!-- Widget tiles matching DaterHome style -->
        <div class="widget-container">
            <div class="widget-tile" @click="$router.push({name: 'CupidDetails', params: {id: user_id}})">
                <span class="material-symbols-outlined icon">person</span>
                <h3>Profile</h3>
                <p>Manage your profile</p>
            </div>
            
            <div class="widget-tile" @click="$router.push({name: 'GigDetails', params: {id: user_id}})">
                <span class="material-symbols-outlined icon">search</span>
                <h3>Active Gigs</h3>
                <p>Search for available gigs</p>
            </div>
            
            <div class="widget-tile" @click="$router.push({name: 'GigComplete', params: {id: user_id}})">
                <span class="material-symbols-outlined icon">assignment_turned_in</span>
                <h3>Past Gigs</h3>
                <p>View completed gigs</p>
            </div>
        </div>

        <!-- Location status indicator -->
        <div v-if="isLoadingLocation" class="location-status loading">
            <span class="material-symbols-outlined">location_searching</span>
            Getting your location...
        </div>
        <div v-else-if="!currentLocation" class="location-status warning">
            <span class="material-symbols-outlined">location_off</span>
            Location unavailable - showing all gigs
        </div>
        <div v-else class="location-status success">
            <span class="material-symbols-outlined">location_on</span>
            Showing gigs within {{ cupidRange }} miles
        </div>

        <!-- Available Gigs Section -->
        <h2 class="section-title">Available</h2>
        <div class="gig-container">
            <div class="gig-tile" v-for="(gig, index) in gigs" :key="gig.id">
                <GigData :gig="gig"/>
                <div class="button-container">
                    <button @click="claim(gig.id)" class="btn-primary">Claim</button>
                    <button @click="openMap(gig)" class="btn-map">Map</button>
                </div>
            </div>
        </div>
        <p v-if="gigs.length == 0" class="empty-message">
            {{ currentLocation ? 'There are no gigs available within your range.' : 'There are no gigs available.' }}
        </p>
    </main>

    <!-- Map Modal -->
    <GigMap 
        v-if="showMap && selectedGig"
        :pickup-location="selectedGig.quest.pickup_location"
        :dropoff-location="selectedGig.quest.dropoff_location"
        :gig-title="`Map for ${selectedGig.quest.items_requested}`"
        @close="closeMap"
    />
</template>

<style scoped>
    /* New color scheme variables - same as other pages */
    main {
        --new-primary: #09A129;     /* Green for text */
        --new-secondary: #1F487E;   /* Dark blue for buttons */
        --new-background: #000000;  /* Black for backgrounds */
        --new-accent: #FB3640;      /* Red */
        --new-light-blue: #00CCFF;  /* Light blue */
        
        padding: 20px;
        background-color: var(--new-background);
        color: var(--new-primary);
        min-height: 100vh;
        
        /* Spacing for Banner and NavBar */
        margin-top: 60px; /* Space for banner (60px) + gap */
    }

    /* Mobile: Add bottom margin for bottom navbar */
    @media (max-width: 768px) {
        main {
            margin-bottom: 90px; /* Space for bottom navbar */
        }
    }

    /* Desktop: Add top margin for navbar below banner */
    @media (min-width: 769px) {
        main {
            margin-top: 140px; /* Space for banner + navbar + gaps */
        }
    }

    .page-title {
        color: var(--new-primary);
        text-align: center;
        margin: 20px auto 30px auto;
        font-size: 2.2em;
        font-weight: bold;
    }

    .section-title {
        color: var(--new-primary);
        margin: 30px 0 20px 0;
        font-size: 1.8em;
        font-weight: bold;
        text-align: center;
    }

    /* Widget tiles - same as DaterHome */
    .widget-container {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin-bottom: 30px;
        justify-content: flex-start;
    }

    /* Mobile: 2 tiles per row */
    @media (max-width: 768px) {
        .widget-container {
            justify-content: space-between;
        }
        
        .widget-tile {
            flex: 0 1 calc(50% - 8px);
            min-width: 120px;
            max-width: 140px;
        }
    }

    /* Tablet: 2 tiles per row (4 total) */
    @media (min-width: 769px) and (max-width: 1024px) {
        .widget-container {
            justify-content: center;
        }
        
        .widget-tile {
            flex: 0 1 calc(50% - 10px);
            min-width: 180px;
            max-width: 200px;
        }
    }

    /* Desktop: 3 tiles per row */
    @media (min-width: 1025px) {
        .widget-container {
            justify-content: center;
        }
        
        .widget-tile {
            flex: 0 1 calc(33% - 12px);
            min-width: 180px;
            max-width: 220px;
        }
    }

    .widget-tile {
        border-radius: 12px;
        padding: 12px;
        border: 2px solid var(--new-primary);
        background-color: var(--new-background);
        box-shadow: 0 4px 8px rgba(9, 161, 41, 0.2);
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        cursor: pointer;
        min-height: 100px;
    }

    .widget-tile:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(9, 161, 41, 0.3);
        border-color: var(--new-light-blue);
    }

    .widget-tile:active {
        transform: translateY(0);
    }

    .icon {
        font-size: 32px;
        color: var(--new-primary);
        margin-bottom: 6px;
    }

    .widget-tile h3 {
        color: var(--new-primary);
        margin: 6px 0 3px 0;
        font-size: 1.0em;
        font-weight: bold;
    }

    .widget-tile p {
        color: var(--new-primary);
        margin: 0;
        font-size: 0.8em;
        opacity: 0.8;
    }

    /* Gig container - same as GigDetails/GigComplete */
    .gig-container {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        margin-bottom: 30px;
        justify-content: flex-start;
    }

    /* Mobile: 2 gig tiles per row */
    @media (max-width: 768px) {
        .gig-container {
            justify-content: space-between;
        }
        
        .gig-tile {
            flex: 0 1 calc(50% - 10px);
            min-width: 140px;
            max-width: 180px;
        }
    }

    /* Tablet: 3 gig tiles per row */
    @media (min-width: 769px) and (max-width: 1024px) {
        .gig-tile {
            flex: 0 1 calc(33.333% - 14px);
            min-width: 200px;
            max-width: 250px;
        }
    }

    /* Desktop: 4 gig tiles per row */
    @media (min-width: 1025px) {
        .gig-tile {
            flex: 0 1 calc(25% - 15px);
            min-width: 220px;
            max-width: 280px;
        }
    }

    /* Large desktop: 5 gig tiles per row */
    @media (min-width: 1400px) {
        .gig-tile {
            flex: 0 1 calc(20% - 16px);
            min-width: 220px;
            max-width: 280px;
        }
    }

    .gig-tile {
        border-radius: 12px;
        padding: 20px;
        border: 2px solid var(--new-secondary);
        background-color: var(--new-background);
        box-shadow: 0 4px 8px rgba(31, 72, 126, 0.3);
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 180px;
    }

    .gig-tile:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(31, 72, 126, 0.4);
        border-color: var(--new-light-blue);
    }

    .button-container {
        margin-top: 15px;
        display: flex;
        gap: 10px;
        justify-content: center;
    }

    .btn-primary {
        background-color: var(--new-secondary);
        color: var(--new-primary);
        border: 2px solid var(--new-primary);
        padding: 8px 16px;
        border-radius: 6px;
        cursor: pointer;
        font-weight: bold;
        transition: all 0.3s ease;
        flex: 1;
    }

    .btn-primary:hover {
        background-color: var(--new-primary);
        color: var(--new-background);
        transform: translateY(-1px);
    }

    .btn-map {
        background-color: var(--new-light-blue);
        color: var(--new-background);
        border: 2px solid var(--new-primary);
        border-radius: 6px;
        padding: 8px 12px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 12px;
        white-space: nowrap;
    }

    .btn-map:hover {
        background-color: var(--new-primary);
        color: var(--new-background);
        transform: translateY(-1px);
    }

    .btn-map:active {
        transform: translateY(0);
    }

    .empty-message {
        text-align: center;
        color: var(--new-primary);
        font-style: italic;
        margin: 40px 0;
        font-size: 1.1em;
    }

    /* Location status styles */
    .location-status {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 10px;
        margin: 10px 0 20px 0;
        border-radius: 8px;
        font-size: 0.9em;
        font-weight: bold;
    }

    .location-status.loading {
        background-color: rgba(0, 204, 255, 0.1);
        color: var(--new-light-blue);
        border: 1px solid var(--new-light-blue);
    }

    .location-status.warning {
        background-color: rgba(251, 54, 64, 0.1);
        color: var(--new-accent);
        border: 1px solid var(--new-accent);
    }

    .location-status.success {
        background-color: rgba(9, 161, 41, 0.1);
        color: var(--new-primary);
        border: 1px solid var(--new-primary);
    }

    .location-status .material-symbols-outlined {
        font-size: 20px;
    }
</style>