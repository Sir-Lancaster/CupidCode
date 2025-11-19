<script setup>
    import { makeRequest } from '../utils/make_request'
    import {ref, onMounted} from 'vue'

    import CupidBanner from './components/CupidBanner.vue';
    import CupidNavBar from './components/CupidNavBar.vue';
    import GigData from './components/GigData.vue'
    import Heart from '../components/Heart.vue'
    import Popup from '../components/Popup.vue'

    const gigs = ref([])
    const popupActive = ref(false)
    const activeGig = ref({})
    const message = ref("")
    const heartState = ref([false,false,false,false,false])
    const rating = ref(0)

    const user_id  = parseInt(window.location.hash.split('/')[4]) //Gets the id from the router

    async function getData() {
        gigs.value = await makeRequest(`api/cupid/gigs/${user_id}?complete=true`)
        //Django returns a 404 if there are none. We have to tell Vue it is ok.
        if (gigs.value.detail === 'Not found.'){
            gigs.value = []
        }
    }

    function toggleActiveGig(gig) {
        if(popupActive.value){
            popupActive.value = false
            activeGig.value = {}
        }
        else{
            popupActive.value = true
            activeGig.value = gig
        }
    }

    function sendReview() {
        makeRequest('api/dater/rate/', 'post', {
            'dater_id':activeGig.value.dater_id,
            'gig_id':activeGig.value.id,
            'message':message.value,
            'rating':rating.value
        })
        toggleActiveGig()
    }

    function checkHeart(e) {
        const target = e.target.parentNode
        const clickedRating = Number(target.dataset.index) + 1
        
        // If clicking on the same heart that represents current rating, reset to 0
        if (clickedRating === rating.value) {
            rating.value = 0
            // Set all hearts to false
            for (let i = 0; i < 5; i++) {
                heartState.value[i] = false
            }
        } else {
            // Set new rating
            rating.value = clickedRating
            // Update heart states
            for (let i = 0; i < rating.value; i++) {
                heartState.value[i] = true
            }
            for (let i = rating.value; i < 5; i++) {
                heartState.value[i] = false
            }
        }
    }

    onMounted(getData)

</script>

<template>
    <CupidBanner />
    <CupidNavBar currentPage="GigComplete" />
    
    <main>
        <h1>Completed Gigs</h1>
        <div class="gig-container">
            <div class="gig-tile" v-for="(gig, index) in gigs" :key="gig.id">
                <GigData :gig="gig"/>
                <div class="button-container">
                    <button @click="toggleActiveGig(gig)" class="btn-primary">Rate Dater</button>
                </div>
            </div>
        </div>
        <p v-if="gigs.length == 0" class="empty-message">No completed gigs yet.</p>
        
        <Popup :data-active="popupActive">
            <h1>Rate</h1>
            <label class="update-content" for="message">
                <textarea id="message" v-model="message"/>
            </label>
            <label class="update-content" for="rating">
                <div class="row" @click="checkHeart">
                    <Heart v-for="i in 5" :data-index="i - 1" :data-active="heartState[i - 1]"/>
                </div>
            </label>
            <div class="popup-buttons">
                <button @click="sendReview" class="btn-primary">Send</button>
                <button @click="toggleActiveGig" class="btn-danger">Cancel</button>
            </div>
        </Popup>
    </main>
</template>

<style scoped>
    main {
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
        }
        
        .gig-tile {
            flex: 0 1 calc(50% - 8px);
            min-width: 280px;
        }
    }

    /* Tablet: 3 tiles per row */
    @media (min-width: 769px) and (max-width: 1024px) {
        .gig-tile {
            flex: 0 1 calc(33.333% - 10px);
            min-width: 250px;
        }
    }

    /* Desktop: 4-5 tiles per row */
    @media (min-width: 1025px) {
        .gig-tile {
            flex: 0 1 calc(25% - 12px);
            min-width: 220px;
            max-width: 300px;
        }
    }

    /* Large desktop: 5 tiles per row */
    @media (min-width: 1400px) {
        .gig-tile {
            flex: 0 1 calc(20% - 12px);
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
        justify-content: center;
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

    h1 {
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

    /* Popup styling updated for new color scheme */
    .popup-buttons {
        display: flex;
        flex-direction: row;
        gap: 16px;
        justify-content: center;
        margin-top: 16px;
    }

    .popup h1 {
        margin: auto;
        margin-top: 12px;
        margin-bottom: 4px;
        width: fit-content;
        color: var(--new-primary);
    }

    .popup div {
        margin: auto;
    }
    
    .row {
        display: flex;
        flex-direction: row;
        justify-content: center;
    }

    .update-content {
        text-align: center;
        margin-bottom: 4px;
        color: var(--new-primary);
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .update-content textarea {
        border: 1px solid var(--new-primary);
        border-radius: 4px;
        padding: 8px;
        background-color: var(--new-background);
        color: var(--new-primary);
        min-width: 250px;
        min-height: 80px;
        resize: vertical;
    }

    .update-content textarea:focus {
        outline: 2px solid var(--new-primary);
        border-color: var(--new-primary);
    }
</style>
