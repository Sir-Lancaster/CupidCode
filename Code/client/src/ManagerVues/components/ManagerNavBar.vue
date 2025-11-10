<script setup>
import router from '../../router'

const props = defineProps(['currentPage'])

function navigateTo(routeName, params = {}) {
  router.push({ name: routeName, params })
}

// Get user_id from URL for navigation
const user_id = parseInt(window.location.hash.split('/')[3])

// Navigation items with their routes and icons
const navItems = [
  { name: 'Dashboard', route: 'ManagerHome', icon: 'dashboard' },
  { name: 'Daters', route: 'ManageDaters', icon: 'favorite' },
  { name: 'Cupids', route: 'ManageCupids', icon: 'person' }
]
</script>

<template>
  <nav class="navbar">
    <button 
      v-for="item in navItems" 
      :key="item.name"
      @click="navigateTo(item.route, { id: user_id })"
      class="nav-button"
      :class="{ active: currentPage === item.route }"
    >
      <span class="nav-icon">
        <span class="material-symbols-outlined">{{ item.icon }}</span>
        <!-- Fallback if Material Icons don't load -->
        <span class="fallback-icon" v-if="false">{{ item.name.charAt(0) }}</span>
      </span>
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
  background-color: #000000 !important;
  border-top: 2px solid #00CCFF;
  border-bottom: 2px solid #00CCFF;
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
  color: #FB3640 !important; /* Red for inactive */
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
  color: #00CCFF !important; /* Light blue for active */
}

.nav-button:hover {
  transform: translateY(-2px);
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
  background-color: #FB3640;
  color: white;
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
    min-width: 60px;
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
