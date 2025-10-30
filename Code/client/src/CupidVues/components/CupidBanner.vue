<script setup>
import { ref } from 'vue'
import router from '../../router'
import { clearUserSession } from '../../utils/auth'
import { makeRequest } from '../../utils/make_request'

const props = defineProps(['title'])
const isDrawerOpen = ref(false)

function toggleDrawer() {
  isDrawerOpen.value = !isDrawerOpen.value
}

function closeDrawer() {
  isDrawerOpen.value = false
}

function navigateTo(routeName) {
    // Get user_id from current route instead of hash extraction
    const currentUserId = router.currentRoute.value.params.id
    
    router.push({ 
        name: routeName, 
        params: { id: currentUserId }
    })
}

async function logout() {
  try {
    // Close drawer first
    closeDrawer()
    
    // Clear frontend session
    clearUserSession()
    
    // Call backend logout endpoint
    await makeRequest('logout/', 'POST')
    
    // Redirect to login page
    router.push({ name: 'Login' })
  } catch (error) {
    console.error('Logout error:', error)
    // Even if backend logout fails, clear frontend session and redirect
    clearUserSession()
    router.push({ name: 'Login' })
  }
}

// Get user_id from URL for navigation
const user_id = parseInt(window.location.hash.split('/')[3])
</script>

<template>
  <div class="banner">
    <button @click="toggleDrawer" class="hamburger-btn">
      <span class="material-symbols-outlined">menu</span>
    </button>
    
    <div class="logo">
      Cupid Code
    </div>
    
    <!-- Side Drawer -->
    <div class="drawer-overlay" :class="{ open: isDrawerOpen }" @click="closeDrawer"></div>
    <div class="drawer" :class="{ open: isDrawerOpen }">
      <div class="drawer-header">
        <h3>Navigation</h3>
        <button @click="closeDrawer" class="close-btn">
          <span class="material-symbols-outlined">close</span>
        </button>
      </div>
      
      <nav class="drawer-nav">
        <button @click="navigateTo('CupidHome', { id: user_id })" class="nav-item">
          <span class="material-symbols-outlined">home</span>
          Home
        </button>
        
        <button @click="navigateTo('GigDetails', { id: user_id })" class="nav-item">
          <span class="material-symbols-outlined">search</span>
          Find Gigs
        </button>
        
        <button @click="navigateTo('GigComplete', { id: user_id })" class="nav-item">
          <span class="material-symbols-outlined">assignment_turned_in</span>
          Completed Gigs
        </button>
        
        <button @click="navigateTo('CupidDetails', { id: user_id })" class="nav-item">
          <span class="material-symbols-outlined">person</span>
          Profile
        </button>
        
        <button @click="navigateTo('CupidFeedback', { id: user_id })" class="nav-item">
          <span class="material-symbols-outlined">notifications</span>
          Notifications
        </button>
        
        <button @click="navigateTo('CupidBalance', { id: user_id })" class="nav-item">
          <span class="material-symbols-outlined">account_balance_wallet</span>
          Balance
        </button>
        
        <button @click="navigateTo('CupidSettings', { id: user_id })" class="nav-item">
          <span class="material-symbols-outlined">settings</span>
          Settings
        </button>
        
        <div class="accessibility-section">
          <h4>Accessibility</h4>
          <button class="nav-item accessibility-toggle">
            <span class="material-symbols-outlined">light_mode</span>
            Toggle Light Mode
          </button>
        </div>
        
        <!-- Logout Section -->
        <div class="logout-section">
          <button @click="logout" class="nav-item logout-btn">
            <span class="material-symbols-outlined">logout</span>
            Logout
          </button>
        </div>
      </nav>
    </div>
  </div>
</template>

<style scoped>
.banner {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background-color: #000000;
  border-top: 2px solid #00CCFF;
  border-bottom: 2px solid #00CCFF;
  display: flex;
  align-items: center;
  padding: 0 16px;
  z-index: 1000;
}

.hamburger-btn {
  background: none;
  border: none;
  color: #09A129;
  font-size: 24px;
  cursor: pointer;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hamburger-btn:hover {
  color: #00CCFF;
}

.logo {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  color: #09A129;
  font-size: 20px;
  font-weight: bold;
}

/* Drawer Styles */
.drawer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  z-index: 1001;
}

.drawer-overlay.open {
  opacity: 1;
  visibility: visible;
}

.drawer {
  position: fixed;
  top: 0;
  left: -300px;
  width: 280px;
  height: 100vh;
  background-color: #000000;
  border-right: 2px solid #00CCFF;
  transition: left 0.3s ease;
  z-index: 1002;
  overflow-y: auto;
}

.drawer.open {
  left: 0;
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #00CCFF;
}

.drawer-header h3 {
  color: #09A129;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: #09A129;
  font-size: 24px;
  cursor: pointer;
  padding: 4px;
}

.close-btn:hover {
  color: #00CCFF;
}

.drawer-nav {
  padding: 16px 0;
}

.nav-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: none;
  border: none;
  color: #09A129;
  font-size: 16px;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s ease;
}

.nav-item:hover {
  background-color: #1F487E;
  color: #00CCFF;
}

.nav-item .material-symbols-outlined {
  font-size: 20px;
}

.accessibility-section {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #00CCFF;
}

.accessibility-section h4 {
  color: #09A129;
  margin: 0 0 12px 16px;
  font-size: 14px;
}

.accessibility-toggle {
  font-style: italic;
}

/* Logout Section */
.logout-section {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #FB3640;
}

.logout-btn {
  color: #FB3640 !important;
  font-weight: bold;
}

.logout-btn:hover {
  background-color: #FB3640 !important;
  color: #000000 !important;
}
</style>
