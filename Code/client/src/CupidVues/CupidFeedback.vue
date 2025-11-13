<script setup>
import { ref, onMounted } from 'vue';
import { makeRequest } from '../utils/make_request';

import CupidBanner from './components/CupidBanner.vue';
import CupidNavBar from './components/CupidNavBar.vue';
import Heart from '../components/Heart.vue';


const user_id  = parseInt(window.location.hash.split('/')[3])

const feedback = ref([])

async function getFeedback() {
    const res = await makeRequest(`/api/cupid/ratings/${user_id}`)
    feedback.value = res
}

onMounted(getFeedback)
</script>

<template>
    <CupidBanner />
    <CupidNavBar currentPage="" />

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

.container {
    margin: 40px;
    margin-top: 50px;
}
.feedback {
    padding: 16px;
    border-radius: 16px;
    margin: 10px;
    display: flex;
    align-items: center;
    flex-direction: column;
}

.even {
    background-color: var(--secondary-blue);
}

.odd {
    background-color: var(--secondary-red);
}

.feedback h1 {
    color: var(--new-primary);
}

.even span {
    background-color: var(--primary-blue);
    padding: 6px;
    border-radius: 4px;
}

.odd span {
    background-color: var(--primary-red);
    padding: 6px;
    border-radius: 4px;
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
