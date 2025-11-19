<script setup>
import router from '../router/index.js'

import Banner from '../components/Banner.vue';
import NavBar from '../components/NavBar.vue';

const user_id  = parseInt(window.location.hash.split('/')[3])

// Navigation functions
function navigateTo(routeName) {
  router.push({ name: routeName, params: { id: user_id } })
}

</script>

<template>
    <Banner />
    <NavBar currentPage="Home" />
    
    <main>
        <h1 class="page-title">Dater Home</h1>
        
        <div class="widget-container">
            <div class="widget-tile" @click="navigateTo('AiChat')">
                <span class="material-symbols-outlined icon">forum</span>
                <h3>AI Chat</h3>
                <p>Chat with AI assistant</p>
            </div>
        
            
            <div class="widget-tile" @click="navigateTo('DaterGigs')">
                <span class="material-symbols-outlined icon">work</span>
                <h3>My Gigs</h3>
                <p>View and manage gigs</p>
            </div>
            
            <div class="widget-tile" @click="navigateTo('CreateGig')">
                <span class="material-symbols-outlined icon">add_circle</span>
                <h3>Create Gig</h3>
                <p>Post a new gig</p>
            </div>
        </div>
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

    .page-title {
        color: var(--new-primary);
        text-align: center;
        margin: 20px auto 30px auto;
        font-size: 2.2em;
        font-weight: bold;
    }

    /* Responsive flexbox container for widget tiles */
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

    /* Desktop: 4 tiles per row */
    @media (min-width: 1025px) {
        .widget-container {
            justify-content: center;
        }
        
        .widget-tile {
            flex: 0 1 calc(25% - 12px);
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

    .widget-tile.help:hover {
        border-color: var(--new-accent);
        box-shadow: 0 6px 12px rgba(251, 54, 64, 0.3);
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
</style>
