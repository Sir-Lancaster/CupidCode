<script setup>
import { defineProps } from 'vue'
import router from '../../router'

const props = defineProps(['currentPage'])

// Get user_id from current route - this is the key fix
const getCurrentUserId = () => {
    return router.currentRoute.value.params.id
}

function navigateTo(routeName, params = {}) {
    if (props.currentPage === routeName) return; // Skip if same page
    
    // Get user_id from current route
    const currentUserId = getCurrentUserId()
    
    // Use the current user ID 
    const navigationParams = {
        id: currentUserId,
        ...params
    }
    
    router.push({ 
        name: routeName, 
        params: navigationParams 
    })
}

// Navigation items array
const navItems = [
    { name: 'Home', route: 'CupidHome', icon: 'home' },
    { name: 'Active Gigs', route: 'GigDetails', icon: 'search' },
    { name: 'Completed Gigs', route: 'GigComplete', icon: 'assignment_turned_in' },
    { name: 'Profile', route: 'CupidDetails', icon: 'person' }
]
</script>

<template>
    <nav class="navbar">
        <button 
            v-for="item in navItems" 
            :key="item.route"
            @click="navigateTo(item.route)"
            :disabled="currentPage === item.route"
            :class="['nav-button', { active: currentPage === item.route }]"
        >
            <span class="material-symbols-outlined">{{ item.icon }}</span>
            <span class="nav-text">{{ item.name }}</span>
        </button>
    </nav>
</template>

<style scoped>
.navbar {
  position: fixed !important;
  left: 0;
  right: 0;
  width: 100%;
  background-color: var(--new-background) !important;
  border-top: 2px solid var(--new-light-blue);
  border-bottom: 2px solid var(--new-light-blue);
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 12px 0;
  z-index: 999;
  height: 70px;
  box-shadow: 0 -2px 10px rgba(0, 204, 255, 0.3);
  margin: 0;
}

/* Mobile: Bottom positioning - FIXED to bottom */
@media (max-width: 768px) {
  .navbar {
    bottom: 0 !important;
    top: auto !important;
  }
}

/* Desktop/Tablet: Below banner - FIXED to top position */
@media (min-width: 769px) {
  .navbar {
    top: 62px !important;
    bottom: auto !important;
  }
}

.nav-button {
  background: none;
  border: none;
  color: var(--new-accent) !important; /* Red for inactive */
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 8px 12px;
  transition: all 0.2s ease;
  width: 90px;
  height: 100%;
}

.nav-button.active {
  color: var(--new-light-blue) !important; /* Light blue for active */
}

.nav-button:hover:not(:disabled) {
  transform: translateY(-2px);
}

.nav-button:disabled {
  cursor: not-allowed;
  opacity: 0.8;
  color: var(--new-light-blue) !important; /* Keep blue color for disabled/active state */
}

.nav-button:disabled:hover {
  transform: none; /* No hover effect when disabled */
}

.nav-icon {
  font-size: 24px;
  margin-bottom: 4px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.nav-text {
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: inherit;
}

.fallback-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: var(--new-accent);
  color: var(--on-button-text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

/* Responsive text sizing */
@media (max-width: 480px) {
  .nav-text {
    font-size: 10px;
  }
  
  .nav-icon {
    font-size: 20px;
  }
  
  .nav-button {
    width: 60px;
    padding: 6px 8px;
  }
}

@media (min-width: 1024px) {
  .nav-text {
    font-size: 14px;
  }
  
  .nav-icon {
    font-size: 28px;
  }
  
  .nav-button {
    width: 110px;
    padding: 12px 16px;
  }
}
</style>
