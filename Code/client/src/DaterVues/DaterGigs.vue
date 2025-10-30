<script setup>
    import { makeRequest } from '../utils/make_request'
    import {ref, onMounted} from 'vue'

    import GigData from './components/GigData.vue'
    import Heart from '../components/Heart.vue'
    import Popup from '../components/Popup.vue'
    import PinkButton from '../components/PinkButton.vue'
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
        rating.value = Number(target.dataset.index) + 1
        for (let i = 0; i <= rating.value; i++){
            heartState.value[i] = true
        }
        for (let i = rating.value; i < 5; i++){
            heartState.value[i] = false
        }
    }

    onMounted(getData)
</script>

<template>
    <Banner />
    <NavBar currentPage="Home" />

    <main>
        <h1>Claimed</h1>
        <hr/>
        <div class="gig-tile" v-for="(gig, index) in claimedGigs">
            <GigData :gig="gig"/>
            <div class="space-evenly">
                <PinkButton @click-forward="cancel(gig.id)">Cancel</PinkButton>
            </div>
        </div>
        <p v-if="claimedGigs.length == 0">You have no active gigs.</p>
        <h1>Unclaimed</h1>
        <hr/>
        <div class="gig-tile" v-for="(gig, index) in unclaimedGigs">
            <GigData :gig="gig"/>
            <div class="space-evenly">
                <PinkButton @click-forward="cancel(gig.id)">Cancel</PinkButton>
            </div>
        </div>
        <p v-if="unclaimedGigs.length == 0">You do not have any pending gigs.</p>
        <h1>Complete</h1>
        <hr/>
        <div class="gig-tile" v-for="(gig, index) in completeGigs">
            <GigData :gig="gig"/>
            <div class="space-evenly">
            <PinkButton @click-forward="toggleActiveGig(gig)">Rate Cupid</PinkButton>
            </div>
        </div>
        <p v-if="completeGigs.length == 0">You have no complete gigs.</p>
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
                <PinkButton class = "margin-sixteen" @click-forward="sendReview">Send</PinkButton>
                <PinkButton class = "margin-sixteen" @click-forward="toggleActiveGig">Cancel</PinkButton>
            </div>
        </Popup>
    </main>
</template>







<style scoped>
    /*main styles*/
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
            margin-bottom: 120px; /* Space for bottom navbar */
        }
    }

    /* Desktop: Add top margin for navbar below banner */
    @media (min-width: 769px) {
        main {
            margin-top: 140px; /* Space for banner + navbar + gaps */
        }
    }





    /*gig styles*/
    .gig-container {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        margin-bottom: 30px;
        justify-content: flex-start;
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
        text-align: center;
    }

    .gig-tile:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(31, 72, 126, 0.4);
        border-color: var(--new-light-blue);
    }





    /*uhhhhhhh other styles? probably rating, which is not implemented yet*/
    .space-evenly {
        display: flex;
        flex-direction: row;
        align-content: center;
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
        color: white;
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




    /*line separator*/
    hr {
        border: 1px solid #F0F0F0;
        border-radius: 30%;
        margin: 6px;
    }
    /* Adjust main padding for mobile */
    main {
        position: absolute;
        top: 0px;
        left: 0px;
        right: 0px;
        padding: 8px;
        padding-bottom: 120px;
        display: flex;
        flex-direction: column;
        align-content: center;
    }
    h1,
    p {
        margin: auto;
    }
</style>


