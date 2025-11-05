<script setup>
    import router from '../router';
    import { makeRequest, logoutRequest } from '../utils/make_request';

    const props = defineProps(['title', 'profile'])
    const user_id  = parseInt(window.location.hash.split('/')[3])

    function openDrawer() {
      const element = document.getElementById('navbar')
      if (element.className === 'navbar') {
        element.className = 'navbar opened'
      }
      else {
        element.className = 'navbar'
      }
    }

    async function logout() {
      await logoutRequest()
      localStorage.clear()
      await router.push('/')
      router.go()
    }

    function naviProf() {
        router.push({ name: props.profile, params: {id: user_id} })
    }
</script>
<template>
    <nav class="nav homenav">
        <button @click="openDrawer" class="icon-button">
            <span id="navMenu" class="material-symbols-outlined icon">menu</span>   
        </button>
        <span id="title">{{ props.title }}</span>
        <button id="profile" class="icon-button" @click="naviProf">
            <span class="material-symbols-outlined icon">account_circle</span>
        </button>
        <div id="navbar" class="navbar">
            <slot />
            <button class="logout" @click="logout"> Logout </button>
        </div>
    </nav>  
</template>
<style>
</style>
