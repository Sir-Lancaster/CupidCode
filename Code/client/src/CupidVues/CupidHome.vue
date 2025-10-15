<script setup>
import {ref, computed} from 'vue';
import router from '../router/index.js'
import { makeRequest } from '../utils/make_request';

import Banner from '../components/Banner.vue';
import CupidNavBar from './components/CupidNavBar.vue';

const user_id  = parseInt(window.location.hash.split('/')[3])

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
    </div>
</template>

<style scoped>
  .container {
    margin: 10px;
    margin-top: 50px;
    display: flex;
    flex-flow: row wrap;
    gap: 10px;
  }

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
