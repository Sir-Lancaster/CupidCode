<script setup>
import { ref, onMounted } from 'vue';
import { makeRequest } from '../utils/make_request';
import router from '../router';

import Banner from '../components/Banner.vue';
import NavBar from '../components/NavBar.vue';
import Heart from '../components/Heart.vue';

const user_id = router.currentRoute.value.params.id

const feedback = ref([])

async function getFeedback() {
    const res = await makeRequest(`/api/dater/ratings/${user_id}`) 
    feedback.value = res
}

onMounted(getFeedback)
</script>

<template>
    <Banner />
    <NavBar currentPage="DaterFeedback" />

    <main>
        <!-- Fixed Header Bar -->
        <div class="header-bar">
            <h1 class="page-title">Feedback</h1>
        </div>

        <div class="container">
            <div v-if="feedback.length === 0" class="empty-state">
                <span class="material-symbols-outlined feedback-icon">feedback</span>
                <h3>No Feedback Yet</h3>
                <p>Complete some gigs to start receiving feedback from Cupids!</p>
            </div>
            
            <div v-else class="feedback-container">
                <div v-for="(item, index) of feedback" :key="index" class="feedback-card">
                    <!-- Hearts Row -->
                    <div class="hearts-row">
                        <Heart v-for="heart in 5" :key="heart" 
                               :data-active="heart <= item.star_rating"/>
                    </div>
                    
                    <!-- Rating Text -->
                    <div class="rating-row">
                        <span class="rating-text">{{ item.star_rating }}/5 Hearts</span>
                    </div>
                    
                    <!-- Feedback Message -->
                    <div class="feedback-message">
                        <p>{{ item.message }}</p>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>

<style scoped>
main {
    background-color: var(--new-background);
    color: var(--new-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;

    /* Spacing for Banner and NavBar */
    margin-top: 60px; /* Space for banner */
    padding-bottom: 120px;
}

/* Mobile: Add bottom padding for bottom navbar */
@media (max-width: 768px) {
    main {
        padding-bottom: 160px; /* Space for navbar */
    }
}

/* Desktop: Add top margin for navbar below banner */
@media (min-width: 769px) {
    main {
        margin-top: 140px; /* Space for banner + navbar + gaps */
        padding-bottom: 40px;
    }
}

/* Fixed Header Bar */
.header-bar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background-color: var(--new-background);
    border-bottom: 2px solid var(--new-primary);
    padding: 16px 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 999;
}

/* Mobile: Position below banner */
@media (max-width: 768px) {
    .header-bar {
        top: 60px; /* Below banner, navbar is at bottom */
    }
}

/* Desktop: Position below banner and navbar */
@media (min-width: 769px) {
    .header-bar {
        top: 140px; /* Below banner + navbar + gaps */
        border-top: 2px solid var(--new-primary);
    }
}

.page-title {
    color: var(--new-primary);
    margin: 0;
    font-size: 2.2em;
    font-weight: bold;
}

@media (max-width: 600px) {
    .page-title {
        font-size: 1.8em;
    }
}

.container {
    flex: 1;
    padding: 20px;
    margin-top: 80px; /* Space for header bar */
}

@media (max-width: 768px) {
    .container {
        margin-top: 60px; /* Adjusted for mobile */
        padding: 12px;
    }
}

/* Empty state styling */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 40px 20px;
    margin-top: 50px;
}

.feedback-icon {
    font-size: 64px;
    color: var(--new-light-blue);
    margin-bottom: 20px;
}

.empty-state h3 {
    color: var(--new-primary);
    margin: 16px 0;
    font-size: 1.4em;
}

.empty-state p {
    color: var(--new-primary);
    opacity: 0.8;
    max-width: 400px;
    line-height: 1.5;
}

/* Feedback container - Grid layout for square cards */
.feedback-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    max-width: 1200px;
    margin: 0 auto;
}

.feedback-card {
    background-color: var(--new-background);
    border: 2px solid var(--new-primary);
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    min-height: 250px; /* Make cards more square */
    aspect-ratio: 1 / 1; /* Force square aspect ratio */
    justify-content: space-between;
}

.feedback-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
    border-color: var(--new-light-blue);
}

/* Hearts Row */
.hearts-row {
    display: flex;
    gap: 4px;
    margin-bottom: 12px;
}

/* Rating Row with Text */
.rating-row {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 12px;
}

.rating-text {
    color: var(--new-primary);
    font-weight: bold;
    font-size: 1.2em;
}


.feedback-message {
    background-color: var(--new-background);
    border-radius: 8px;
    padding: 12px;
    flex: 1;
    display: flex;
    align-items: center;
    width: 100%;
    border: 1px solid var(--new-primary);
}

.feedback-message p {
    margin: 0;
    color: var(--new-primary);
    line-height: 1.4;
    white-space: pre-wrap;
    font-size: 0.95em;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .feedback-container {
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 16px;
    }
    
    .feedback-card {
        padding: 16px;
        min-height: 220px;
    }
    
    .rating-text {
        font-size: 1.1em;
    }
}

@media (max-width: 480px) {
    .feedback-container {
        grid-template-columns: 1fr;
        gap: 12px;
    }
    
    .feedback-card {
        padding: 14px;
        min-height: 200px;
    }
}
</style>
