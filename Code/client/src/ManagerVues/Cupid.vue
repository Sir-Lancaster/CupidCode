<script setup>
import { ref, onMounted } from 'vue';
import { makeRequest } from '../utils/make_request';

import ManagerBanner from './components/ManagerBanner.vue';
import ManagerNavBar from './components/ManagerNavBar.vue';

const cupids = ref([{ }])
const cupidCount = ref(0)

const user_id  = parseInt(window.location.hash.split('/')[3]) //Gets the id from the router

async function getCupids() {
  const res = await makeRequest('/api/manager/cupids/')
  cupids.value = res
  
  // Calculate count properly - if res is an object, count its keys
  if (res && typeof res === 'object') {
    cupidCount.value = Object.keys(res).length
  } else if (Array.isArray(res)) {
    cupidCount.value = res.length
  } else {
    cupidCount.value = 0
  }
}

async function suspend(id) {
  const header = document.getElementById(`header-${id}`)
  const button = document.getElementById(`button-${id}`)
  
  if (header.attributes.class.value.includes('suspended')) {
    header.setAttribute('class', 'tile-header')
    button.innerText = 'Suspend'
    const res = await makeRequest('/api/manager/unsuspend/', 'post', {
      user_id: id,
      role: 'Cupid'
    })
  }
  else {
    header.setAttribute('class', 'tile-header suspended')
    button.innerText = 'Unsuspend'
    const res = await makeRequest('/api/manager/suspend/', 'post', {
      user_id: id,
      role: 'Cupid'
    })
  }
}
  
onMounted(getCupids)
</script>

<template>
  <ManagerBanner />
  <ManagerNavBar currentPage="ManageCupids" />

  <main>
    <!-- Fixed Header Bar -->
    <div class="header-bar">
      <h1 class="page-title">Manage Cupids</h1>
      <div class="cupid-count">
        <span class="count-number">{{ cupidCount }}</span>
        <span class="count-label">Total Cupids</span>
      </div>
    </div>

    <div class="container">
      <div v-if="cupids.length === 0" class="empty-state">
        <span class="material-symbols-outlined cupid-icon">person</span>
        <h3>No Cupids Found</h3>
        <p>There are currently no cupids in the system.</p>
      </div>

      <div v-else class="cupid-container">
        <div v-for="cupid of cupids" :key="cupid.user ? cupid.user['id'] : ''" class="cupid-tile">
          <!-- Header Section -->
          <div class="tile-header" :id="`header-${cupid.user ? cupid.user['id'] : ''}`">
            <span class="material-symbols-outlined">person</span>
            <div class="cupid-info">
              <h3 class="cupid-name">{{ cupid.user ? (cupid.user['first_name'] + " " + cupid.user['last_name']) : 'Unknown' }}</h3>
              <span class="cupid-id">ID: {{ cupid.user ? cupid.user['id'] : 'N/A' }}</span>
            </div>
          </div>

          <!-- Content Section -->
          <div class="tile-content">
            <div class="info-row">
              <span class="info-label">Email:</span>
              <span class="info-value">{{ cupid.user ? cupid.user['email'] : 'N/A' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Rating:</span>
              <span class="info-value">{{ cupid.rating_sum || 'No ratings' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Location:</span>
              <span class="info-value">{{ cupid.location || 'Not specified' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Completed Gigs:</span>
              <span class="info-value">{{ cupid.gigs_completed || 0 }}</span>
            </div>
          </div>

          <!-- Action Section -->
          <div class="tile-actions">
            <button 
              :id="`button-${cupid.user ? cupid.user['id'] : ''}`" 
              class="action-button suspend-btn" 
              @click="() => suspend(cupid.user ? cupid.user['id'] : '')">
              Suspend
            </button>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
/* New color scheme variables */
main {
  --new-primary: #09A129;     /* Green for text */
  --new-secondary: #1F487E;   /* Dark blue for buttons */
  --new-background: #000000;  /* Black for backgrounds */
  --new-accent: #FB3640;      /* Red */
  --new-light-blue: #00CCFF;  /* Light blue */
  
  background-color: var(--new-background);
  color: var(--new-primary);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  
  /* Spacing for Banner and NavBar */
  margin-top: 60px;
  padding-bottom: 120px;
}

/* Mobile: Add bottom padding for bottom navbar */
@media (max-width: 768px) {
  main {
    padding-bottom: 160px;
  }
}

/* Desktop: Add top margin for navbar below banner */
@media (min-width: 769px) {
  main {
    margin-top: 140px;
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
  justify-content: space-between;
  align-items: center;
  z-index: 999;
}

@media (max-width: 768px) {
  .header-bar {
    top: 60px;
    flex-direction: column;
    gap: 8px;
    padding: 12px 20px;
  }
}

@media (min-width: 769px) {
  .header-bar {
    top: 140px;
    border-top: 2px solid var(--new-primary);
  }
}

.page-title {
  color: var(--new-primary);
  margin: 0;
  font-size: 2.2em;
  font-weight: bold;
}

.cupid-count {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.count-number {
  font-size: 1.8em;
  font-weight: bold;
  color: var(--new-light-blue);
}

.count-label {
  font-size: 0.9em;
  color: var(--new-primary);
  opacity: 0.8;
}

.container {
  flex: 1;
  padding: 20px;
  margin-top: 80px;
  max-width: 1400px;
  margin-left: auto;
  margin-right: auto;
}

@media (max-width: 768px) {
  .container {
    margin-top: 100px;
    padding: 12px;
  }
}

/* Empty state */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 40px 20px;
  margin-top: 50px;
}

.cupid-icon {
  font-size: 64px;
  color: var(--new-secondary);
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

/* Cupid container - Grid layout */
.cupid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .cupid-container {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}

/* Cupid tiles */
.cupid-tile {
  background-color: var(--new-secondary);
  border: 2px solid var(--new-primary);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.cupid-tile:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
  border-color: var(--new-light-blue);
}

/* Tile header */
.tile-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--new-primary);
}

.tile-header.suspended {
  border-color: var(--new-accent);
  color: var(--new-accent);
}

.tile-header .material-symbols-outlined {
  font-size: 28px;
  color: var(--new-secondary);
}

.cupid-info {
  flex: 1;
}

.cupid-name {
  margin: 0;
  color: var(--new-primary);
  font-size: 1.2em;
  font-weight: bold;
}

.cupid-id {
  color: var(--new-primary);
  opacity: 0.7;
  font-size: 0.9em;
}

/* Tile content */
.tile-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.info-label {
  font-weight: bold;
  color: var(--new-primary);
  min-width: 80px;
}

.info-value {
  color: var(--new-primary);
  opacity: 0.9;
  text-align: right;
  flex: 1;
}

/* Tile actions */
.tile-actions {
  display: flex;
  justify-content: center;
  padding-top: 12px;
  border-top: 1px solid var(--new-primary);
}

.action-button {
  padding: 10px 20px;
  border-radius: 8px;
  border: 2px solid;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 120px;
}

.suspend-btn {
  background-color: var(--new-accent);
  border-color: var(--new-accent);
  color: white;
}

.suspend-btn:hover {
  background-color: white;
  color: var(--new-accent);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .page-title {
    font-size: 1.8em;
  }
  
  .cupid-tile {
    padding: 16px;
  }
  
  .info-row {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .info-value {
    text-align: left;
  }
}
</style>
