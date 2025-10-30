<script setup>
import router from './router/index.js';
import { makeRequest } from './utils/make_request.js';

const user_id = parseInt(window.location.hash.split('/')[3])

async function getUser() {
  const results = await makeRequest('api/user/', 'get', {
    user_id: user_id
  })
}
</script>

<template>
    <div id="app">
    </div>
    <router-view />
</template>

<style scoped>

</style>
