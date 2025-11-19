<script setup>
    import { makeRequest } from '../utils/make_request'
    import {ref, onMounted} from 'vue'

    import GigData from './components/GigData.vue'
    import Heart from '../components/Heart.vue'
    import Popup from '../components/Popup.vue'
    import Banner from '../components/Banner.vue';
    import NavBar from '../components/NavBar.vue';

    // Gig lists
    const claimedGigs = ref([])
    const unclaimedGigs = ref([])
    const completeGigs = ref([])

    //Review popup
    const popupActive = ref(false)
    const activeGig = ref({})
    const message = ref("")
    const heartState = ref([false,false,false,false,false])
    const rating = ref(0)


    const user_id  = parseInt(window.location.hash.split('/')[3]) //Gets the id from the router

    async function getData() {
        let gigs = await makeRequest(`api/dater/gigs/${user_id}`)
        //Django returns a 404 if there none of either of these. We have to tell Vue it is ok.
        if (gigs.detail === 'Not found.'){
            gigs = []
        }
        unclaimedGigs.value = []
        claimedGigs.value = []
        completeGigs.value = []
        gigs.forEach( gig => {
            if (gig.status == 0){
                unclaimedGigs.value.push(gig)
            } else if (gig.status == 1) {
                claimedGigs.value.push(gig)
            } else if (gig.status == 2) {
                completeGigs.value.push(gig)
            }
        })
    }

    async function cancel(id) {
        await makeRequest('/api/gig/cancel/','post',{
            'gig_id':id
        })
        getData()
    }

    async function complete(id) {
        try {
            const response = await makeRequest('/api/gig/complete/', 'post', {
                'gig_id': id
            })
            getData()
        } catch (error) {
            console.error('Error completing gig:', error)
            alert('Failed to complete gig. Please try again.')
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
        makeRequest('api/cupid/rate/', 'post', {
            'cupid_id':activeGig.value.cupid_id,
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
    <Banner />
    <NavBar currentPage="Home" />

    <main>
        <h1>Unclaimed</h1>
        <hr/>
        <div class="gig-container">
            <div class="gig-tile" v-for="(gig, index) in unclaimedGigs" :key="gig.id">
                <GigData :gig="gig"/>
                <div class="button-container">
                    <button @click="cancel(gig.id)" class="action-button cancel-button">Cancel</button>
                </div>
            </div>
        </div>
        <p v-if="unclaimedGigs.length == 0" class="empty-message">You do not have any pending gigs.</p>


        <h1>Claimed</h1>
        <hr/>
        <div class="gig-container">
            <div class="gig-tile" v-for="(gig, index) in claimedGigs" :key="gig.id">
                <GigData :gig="gig"/>
                <div class="button-container">
                    <button @click="cancel(gig.id)" class="action-button cancel-button">Cancel</button>
                    <button @click="complete(gig.id)" class="submit-btn">Complete</button>
                </div>
            </div>
        </div>
        <p v-if="claimedGigs.length == 0" class="empty-message">You have no active gigs.</p>
        

        <h1>Complete</h1>
        <hr/>
        <div class="gig-container">
            <div class="gig-tile" v-for="(gig, index) in completeGigs" :key="gig.id">
                <GigData :gig="gig"/>
                <div class="button-container">
                    <button @click="toggleActiveGig(gig)" class="action-button rate-button">Rate Cupid</button>
                </div>
            </div>
        </div>
        <p v-if="completeGigs.length == 0" class="empty-message">You have no complete gigs.</p>
        
        <Popup :data-active="popupActive">
            <h1>Rate</h1>
            <label class="update-content" for="message">
                <textarea id="message" v-model="message"/>
            </label>
            <label class="update-content" for="rating">
                <div class="heart-row" @click="checkHeart">
                    <Heart v-for="i in 5" :data-index="i - 1" :data-active="heartState[i - 1]"/>
                </div>
            </label>
            <div class="space-evenly">
                <button @click="sendReview" class="action-button send-button margin-sixteen">Send</button>
                <button @click="toggleActiveGig" class="action-button cancel-button margin-sixteen">Cancel</button>
            </div>
        </Popup>
    </main>
</template>

<style scoped>
    /*main styles*/
    main {
        padding: 20px;
        background-color: var(--new-background);
        color: var(--new-primary);
        min-height: 100vh;

        /* Fixed spacing for Banner and NavBar */
        padding-top: 80px; /* Space for banner + navbar + gap */
        margin-top: 0;
    }

    /* Mobile: Add bottom margin for bottom navbar */
    @media (max-width: 768px) {
        main {
            padding-top: 60px; /* Space for banner + extra spacing on mobile */
            padding-bottom: 140px; /* Space for bottom navbar */
        }
    }

    /* Desktop: Add top margin for navbar below banner */
    @media (min-width: 769px) {
        main {
            padding-top: 160px; /* Space for banner + navbar + gaps */
        }
    }


    /*gig styles*/
    .gig-container {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin-bottom: 30px;
        justify-content: flex-start;
    }

    /* Mobile: 1-2 tiles per row */
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
                min-height: 180px;
            }
        }
    }

    /* Tablet: 2-3 tiles per row */
    @media (min-width: 769px) and (max-width: 1024px) {
        .gig-tile {
            flex: 0 1 calc(33.333% - 10px);
            min-width: 250px;
        }
    }

    /* Desktop: 3-4 tiles per row */
    @media (min-width: 1025px) {
        .gig-tile {
            flex: 0 1 calc(25% - 12px);
            min-width: 220px;
            max-width: 300px;
        }
    }

    /* Large desktop: 4-5 tiles per row */
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
        min-height: 200px;
        width: 100%; /* Ensure full width within flex constraints */
        box-sizing: border-box; /* Include padding and border in width calculation */
    }

    .gig-tile:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(9, 161, 41, 0.3);
        border-color: var(--new-light-blue);
    }

    .button-container {
        display: flex;
        flex-direction: row;
        gap: 10px;
        justify-content: center;
        margin-top: auto;
        padding-top: 15px;
    }

    .empty-message {
        text-align: center;
        color: var(--new-primary);
        font-style: italic;
        margin: 20px auto;
        opacity: 0.8;
    }





    /*uhhhhhhh other styles? probably rating, which is not implemented yet*/
    .space-evenly {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        width: 100%;
    }

    .margin-sixteen{
        margin: 16px;
    }

    .popup h1 {
        margin: auto;
        margin-top: 12px;
        margin-bottom: 4px;
        width: fit-content;
    }

    .popup div {
        margin: auto;
    }

    .heart-row {
        display: flex;
        flex-direction: row;
        width: 100%;
    }

    .active {
        transform: scale(1);
        transition: transform 0.2s cubic-bezier(0,1.4,1,1);
    }

    .update-content {
        text-align: center;
        margin-bottom: 4px;
        color: var(--new-primary);
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .update-content input{
        border: none;
        border-radius: 4px;
        padding: 8px;
    }

    textarea {
        width: 100%;
        min-height: 5em;
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




    /*line separator*/
    hr {
        border: 1px solid var(--new-primary);
        border-radius: 30%;
        margin: 15px auto 20px auto;
        width: 80%;
        opacity: 0.6;
    }
    
    h1,
    p {
        margin: 16px auto;
        text-align: center;
    }

    /* Custom Action Buttons */
    .action-button {
        background-color: var(--new-secondary);
        border: 2px solid var(--new-primary);
        border-radius: 8px;
        padding: 12px 20px;
        color: var(--new-primary);
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 44px;
        min-width: 100px;
    }

    .action-button:hover {
        background-color: var(--new-primary);
        color: var(--new-background);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(9, 161, 41, 0.3);
    }

    .action-button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(9, 161, 41, 0.2);
    }

    .submit-btn {
        padding: 12px 20px;
        background-color: var(--new-secondary);
        color: var(--new-primary);
        border: 2px solid var(--new-primary);
        border-radius: 8px;
        font-size: 16px;
        cursor: pointer;
        font-weight: bold;
        min-height: 44px;
        min-width: 100px;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .submit-btn:hover {
        background-color: var(--new-primary);
        color: var(--new-background);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(9, 161, 41, 0.3); 
    }

    /* Specific button variants */
    .cancel-button {
        background-color: var(--new-accent);
        border-color: var(--new-accent);
        color: var(--on-button-text);
    }

    .cancel-button:hover {
        background-color: var(--on-button-text);
        color: var(--new-accent);
        border-color: var(--new-accent);
    }

    .rate-button {
        background-color: var(--new-light-blue);
        border-color: var(--new-light-blue);
        color: var(--new-background);
    }

    .rate-button:hover {
        background-color: var(--new-background);
        color: var(--new-light-blue);
        border-color: var(--new-light-blue);
    }

    .send-button {
        background-color: var(--new-secondary);
        border-color: var(--new-primary);
    }
</style>


