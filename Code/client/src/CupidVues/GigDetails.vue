<script setup>
    import router from '../router/index'
    import { makeRequest } from '../utils/make_request'
    import {ref, onMounted} from 'vue'

    import NavSuite from '../components/NavSuite.vue';
    import GigData from './components/GigData.vue'

    const gigCount = 0
    const gigs = ref([])
    const activeGigs = ref([])
    const reward = ref(0)
    const rewardShow = ref(false)

    const user_id  = parseInt(window.location.hash.split('/')[3]) //Gets the id from the router

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
    <!-- NavSuite removed as requested - someone else building banner/nav -->
    
    <main>
        <h1>Active</h1>
        <hr/>
        <div class="gig-container">
            <div class="gig-tile active" v-for="(gig, index) in activeGigs" :key="gig.id">
                <GigData :gig="gig"/>
                <div class="button-container">
                    <button @click="complete(gig.id)" class="btn-primary">Complete</button>
                    <button @click="drop(gig.id)" class="btn-danger">Drop</button>
                </div>
            </div>
        </div>
        <p v-if="activeGigs.length == 0" class="empty-message">You are not currently on any gigs.</p>
        
        <h1>Available</h1>
        <hr/>
        <div class="gig-container">
            <div class="gig-tile inactive" v-for="(gig, index) in gigs" :key="gig.id">
                <GigData :gig="gig"/>
                <div class="button-container">
                    <button @click="claim(gig.id)" class="btn-primary">Claim</button>
                </div>
            </div>
        </div>
        <p v-if="gigs.length == 0" class="empty-message">There are no gigs available.</p>
        <p class="bottom" :data-active="rewardShow" v-show="rewardShow">+ ${{ reward.toFixed(2) }}</p>
    </main>
</template>

<style scoped>
    /* New color scheme variables - same as CreateGig page */
    main {
        --new-primary: #09A129;     /* Green for text */
        --new-secondary: #1F487E;   /* Dark blue for buttons */
        --new-background: #000000;  /* Black for backgrounds */
        --new-accent: #FB3640;      /* Red */
        --new-light-blue: #00CCFF;  /* Light blue */
        
        position: absolute;
        top: 42px;
        left: 0px;
        right: 0px;
        padding: 20px;
        background-color: var(--new-background);
        color: var(--new-primary);
        min-height: 100vh;
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

    .empty-message {
        text-align: center;
        color: var(--new-primary);
        font-style: italic;
        margin: 20px auto;
        opacity: 0.8;
    }
</style>
