<script setup>
import {ref, onMounted, computed} from 'vue';
import router from '../router/index.js'
import { makeRequest } from '../utils/make_request';

import CupidBanner from './components/CupidBanner.vue';
import CupidNavBar from './components/CupidNavBar.vue';
import GigData from './components/GigData.vue'

const user_id  = parseInt(window.location.hash.split('/')[3])
const gigCount = 0
    const gigs = ref([])
    const activeGigs = ref([])
    const reward = ref(0)
    const rewardShow = ref(false)

    async function getData() {
        gigs.value = await makeRequest(`api/gig/${user_id}/${gigCount}`)
        activeGigs.value = await makeRequest(`api/cupid/gigs/${user_id}?complete=false`)
        //Django returns a 404 if there none of either of these. We have to tell Vue it is ok.
        if (gigs.value.detail === 'Not found.'){
            gigs.value = []
        }
        if (activeGigs.value.detail === 'Not found.'){
            activeGigs.value = []
        }
    }

    function displayReward(amount) {
        reward.value = amount
        rewardShow.value = true
        setTimeout(() => {rewardShow.value = false},1500)
    }

    async function claim(id) {
        await makeRequest('/api/gig/accept/','post',{
            'gig_id':id
        })
        getData()
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
                <h3>Find Gigs</h3>
                <p>Search for available gigs</p>
            </div>
            
            <div class="widget-tile" @click="$router.push({name: 'GigComplete', params: {id: user_id}})">
                <span class="material-symbols-outlined icon">assignment_turned_in</span>
                <h3>Past Gigs</h3>
                <p>View completed gigs</p>
            </div>
        </div>

        <!-- Available Gigs Section -->
        <h2 class="section-title">Available</h2>
        <div class="gig-container">
            <div class="gig-tile" v-for="(gig, index) in gigs" :key="gig.id">
                <GigData :gig="gig"/>
                <div class="button-container">
                    <button @click="claim(gig.id)" class="btn-primary">Claim</button>
                </div>
            </div>
        </div>
        <p v-if="gigs.length == 0" class="empty-message">There are no gigs available.</p>
    </main>
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
    }

    .btn-primary:hover {
        background-color: var(--new-primary);
        color: var(--new-background);
        transform: translateY(-1px);
    }

    .empty-message {
        text-align: center;
        color: var(--new-primary);
        font-style: italic;
        margin: 40px 0;
        font-size: 1.1em;
    }
</style>
