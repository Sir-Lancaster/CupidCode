<script setup>
import {ref, onMounted, computed} from 'vue';
import router from '../router/index.js'
import { makeRequest } from '../utils/make_request';

import Banner from '../components/Banner.vue';
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
    <Banner />
    <CupidNavBar currentPage="CupidHome" />


    <div class="container">
      <div class="widget red">
        <span class="material-symbols-outlined icon">person</span>
        <router-link class="link" :to="{name: 'CupidDetails', params: {id: user_id}}"> Profile </router-link>
      </div>
      <div class="widget blue">
        <span class="material-symbols-outlined icon">explore</span>
        <router-link id="find" class="link" :to="{name: 'GigDetails', params: {id: user_id}}"> Find Gigs </router-link>
      </div>
      <div class="widget red"> <!-- This will become Calendar when it's made -->
        <span class="material-symbols-outlined icon">playlist_add_check</span>
        <router-link class="link" :to="{name: 'GigComplete', params: {id: user_id}}"> Past Gigs </router-link>
      </div>
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
    </div>
</template>

<style scoped>

  /* New color scheme variables for testing */
  .container {
    --new-primary: #09A129;     /* Green for text */
    --new-secondary: #1F487E;   /* Dark blue for buttons */
    --new-background: #000000;  /* Black for backgrounds */
    --new-accent: #FB3640;      /* Red (not used here) */
    --new-light-blue: #00CCFF;  /* Light blue (not used here) */
    
    display: flex;
    flex-direction: column;
    flex-flow: row wrap;
    gap: 10px;
    align-items: flex-start;
    padding: 20px;
    background-color: var(--new-background);
    color: var(--new-primary);
    min-height: 100vh;
    
    
    /* Spacing for Banner and NavBar */
    margin-top: 60px; /* Space for banner (60px) + gap */
  }

  /* Mobile: Add bottom margin for bottom navbar */
  @media (max-width: 768px) {
    .container {
      margin-bottom: 90px; /* Space for bottom navbar */
    }
  }

  /* Desktop: Add top margin for navbar below banner */
  @media (min-width: 769px) {
    .container {
      margin-top: 140px; /* Space for banner + navbar + gaps */
    }
  }

  /*.container {
    margin: 10px;
    margin-top: 50px;
  }*/

  .widget {
    display: flex;
    flex-flow: column nowrap;
    align-items: center;
    justify-content: center;
    padding: 50px;
    border: none;
    border-radius: 16px;
  }

  .header {
    color: white;
  }

  .blue {
    background-color: var(--secondary-blue);
  }

  .red {
    background-color: var(--secondary-red);
  }
</style>
