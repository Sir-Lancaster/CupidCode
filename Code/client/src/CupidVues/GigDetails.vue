<script setup>
    import router from '../router/index'
    import { makeRequest } from '../utils/make_request'
    import {ref, onMounted} from 'vue'
    import { getCurrentLocation, filterGigsByRange } from '../utils/location_utils';

    import CupidBanner from './components/CupidBanner.vue';
    import CupidNavBar from './components/CupidNavBar.vue';
    import GigData from './components/GigData.vue'
    import GigMap from './GigMap.vue'

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

    const user_id  = parseInt(window.location.hash.split('/')[3]) //Gets the id from the router

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

    function closeMap() {
        showMap.value = false
        selectedGig.value = null
    }

    async function claim(id) {
        await makeRequest('/api/gig/accept/','post',{
            'gig_id':id
        })
        getData()
    }

    async function complete(id) {
        const response = await makeRequest('/api/gig/complete/','post',{
            'gig_id':id
        })
        getData()
        displayReward(response.reward)
    }

    async function drop(id) {
        await makeRequest('/api/gig/drop/','post',{
            'gig_id':id
        })
        getData()
    }

    onMounted(getData)
</script>

<template>
    <CupidBanner />
    <CupidNavBar currentPage="GigDetails" />
    
    <main>
        <h1 class="page-title">Find Gig</h1>
        
        <h2>Active</h2>
        <hr/>
        <div class="gig-container">
            <div class="gig-tile active" v-for="(gig, index) in activeGigs" :key="gig.id">
                <GigData :gig="gig"/>
                <div class="button-container">
                    <button @click="complete(gig.id)" class="btn-primary">Complete</button>
                    <button @click="drop(gig.id)" class="btn-danger">Drop</button>
                    <button @click="openMap(gig)" class="btn-map">Map</button>
                </div>
            </div>
        </div>
        <p v-if="activeGigs.length == 0" class="empty-message">You are not currently on any gigs.</p>
        
        <h2>Available</h2>
        <hr/>
        <div class="gig-container">
            <div class="gig-tile inactive" v-for="(gig, index) in gigs" :key="gig.id">
                <GigData :gig="gig"/>
                <div class="button-container">
                    <button @click="claim(gig.id)" class="btn-primary">Claim</button>
                    <button @click="openMap(gig)" class="btn-map">Map</button>
                </div>
            </div>
        </div>
        <p v-if="gigs.length == 0" class="empty-message">There are no gigs available.</p>
        <p class="bottom" :data-active="rewardShow" v-show="rewardShow">+ ${{ reward.toFixed(2) }}</p>
    </main>

    <!-- Map Modal -->
    <GigMap 
        v-if="showMap && selectedGig"
        :pickup-location="selectedGig.quest.pickup_location"
        :dropoff-location="selectedGig.quest.dropoff_location"
        :gig-title="`Map for ${selectedGig.quest.items_requested}`"
        :cupid-id="user_id"
        @close="closeMap"
    />
</template>

<style scoped>
    /* New color scheme variables - same as CreateGig page */
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

    /* Responsive flexbox container for gig tiles */
    .gig-container {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin-bottom: 30px;
        justify-content: flex-start;
    }

    /* Mobile: 2 tiles per row */
    @media (max-width: 768px) {
        .gig-container {
            justify-content: space-between;
            gap: 10px;
        }
        
        .gig-tile {
            flex: 0 1 calc(50% - 5px);
            min-width: 0; /* Remove minimum width constraint */
            max-width: calc(50% - 5px);
        }
        
        /* Single column on very small screens */
        @media (max-width: 600px) {
            .gig-tile {
                flex: 0 1 100%;
                min-width: 0;
                max-width: 100%;
            }
        }
        
        /* Extra small screens */
        @media (max-width: 400px) {
            .gig-container {
                gap: 8px;
            }
            
            .gig-tile {
                padding: 12px;
            }
        }
    }

    .gig-tile {
        border-radius: 12px;
        padding: 15px;
        border: 2px solid var(--new-primary);
        background-color: var(--new-background);
        box-shadow: 0 4px 8px rgba(9, 161, 41, 0.2);
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        width: 100%; /* Ensure full width within flex constraints */
        box-sizing: border-box; /* Include padding and border in width calculation */
    }

    .gig-tile:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(9, 161, 41, 0.3);
        border-color: var(--new-light-blue);
    }

    .gig-tile h1 {
        margin: 0 0 10px 0;
        color: var(--new-primary);
        font-size: 1.2em;
    }

    .button-container {
        display: flex;
        flex-direction: row;
        gap: 10px;
        justify-content: space-evenly;
        margin-top: auto;
        padding-top: 15px;
    }

    /* Clean button styling for new color scheme */
    .btn-primary {
        background-color: var(--new-secondary);
        color: var(--new-primary);
        border: 1px solid var(--new-primary);
        border-radius: 4px;
        padding: 10px 16px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 14px;
    }

    .btn-primary:hover {
        background-color: var(--new-primary);
        color: var(--new-background);
        transform: translateY(-1px);
    }

    .btn-primary:active {
        transform: translateY(0);
    }

    .btn-danger {
        background-color: var(--new-accent);
        color: var(--new-secondary);
        border: 1px solid var(--new-primary);
        border-radius: 4px;
        padding: 10px 16px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 14px;
    }

    .btn-danger:hover {
        background-color: var(--new-primary);
        color: var(--new-background);
        transform: translateY(-1px);
    }

    .btn-danger:active {
        transform: translateY(0);
    }

        .btn-map {
        background-color: var(--new-light-blue);
        color: var(--new-background);
        border: 1px solid var(--new-primary);
        border-radius: 4px;
        padding: 8px 12px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.2s ease;
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

    .active {
        border-color: var(--new-accent);
        box-shadow: 0 4px 8px rgba(251, 54, 64, 0.2);
    }

    .active:hover {
        border-color: var(--new-accent);
        box-shadow: 0 6px 12px rgba(251, 54, 64, 0.3);
    }

    .inactive {
        border-color: var(--new-secondary);
        box-shadow: 0 4px 8px rgba(31, 72, 126, 0.2);
    }

    .inactive:hover {
        border-color: var(--new-light-blue);
        box-shadow: 0 6px 12px rgba(0, 204, 255, 0.3);
    }

    @keyframes reward {
        from {
            bottom: 0;
            color: var(--new-primary);
        }
        to {
            bottom: 2em;
            color: transparent;
        }
    }

    .bottom {
        position: fixed;
        height: 2em;
        width: 200px;
        bottom: -2em;
        left: 50%;
        margin-left: -100px;
        color: var(--new-primary);
        font-size: 3em;
        text-align: center;
        font-weight: bold;
        z-index: 1000;
    }

    .bottom[data-active="true"] {
        bottom: 2em;
        animation-name: reward;
        animation-duration: 1.5s;
        animation-timing-function: linear;
    }

    hr {
        border: 1px solid var(--new-primary);
        border-radius: 30%;
        margin: 15px auto 20px auto;
        width: 80%;
        opacity: 0.6;
    }

    h1 {
        color: var(--new-primary);
        text-align: center;
        margin: 20px auto 10px auto;
        font-size: 1.8em;
    }

    .page-title {
        color: var(--new-primary);
        text-align: center;
        margin: 20px auto 30px auto;
        font-size: 2.2em;
        font-weight: bold;
    }

    h2 {
        color: var(--new-primary);
        text-align: center;
        margin: 20px auto 10px auto;
        font-size: 1.8em;
    }

    .empty-message {
        text-align: center;
        color: var(--new-primary);
        font-style: italic;
        margin: 20px auto;
        opacity: 0.8;
    }
</style>
