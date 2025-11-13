<script setup>
import { ref, onMounted } from 'vue'
import router from '../../router'
import { clearUserSession } from '../../utils/auth'
import { makeRequest } from '../../utils/make_request'

const props = defineProps(['title'])
const isDrawerOpen = ref(false)
const theme = ref('dark')

function toggleDrawer() {
  isDrawerOpen.value = !isDrawerOpen.value
}

function closeDrawer() {
  isDrawerOpen.value = false
}

function navigateTo(routeName, params = {}) {
  router.push({ name: routeName, params })
  closeDrawer()
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

function applyTheme(t) {
  try {
    document.documentElement.setAttribute('data-theme', t)
    localStorage.setItem('theme', t)
    theme.value = t
  } catch (e) {
    console.warn('Could not apply theme', e)
  }
}

function toggleLightMode() {
  const next = theme.value === 'light' ? 'dark' : 'light'
  applyTheme(next)
}

onMounted(() => {
  const stored = localStorage.getItem('theme')
  if (stored === 'light' || stored === 'dark') {
    applyTheme(stored)
  } else {
    applyTheme('dark')
  }
})
</script>

<template>
  <div class="banner">
    <button @click="toggleDrawer" class="hamburger-btn">
      <span class="material-symbols-outlined">menu</span>
    </button>
    
    <div class="logo">
      Cupid Code Manager
    </div>
    
    <!-- Side Drawer -->
    <div class="drawer-overlay" :class="{ open: isDrawerOpen }" @click="closeDrawer"></div>
    <div class="drawer" :class="{ open: isDrawerOpen }">
      <div class="drawer-header">
        <h3>Manager Navigation</h3>
        <button @click="closeDrawer" class="close-btn">
          <span class="material-symbols-outlined">close</span>
        </button>
      </div>
      
      <nav class="drawer-nav">
        <button @click="navigateTo('ManagerHome', { id: user_id })" class="nav-item">
          <span class="material-symbols-outlined">dashboard</span>
          Dashboard
        </button>
        
        <button @click="navigateTo('ManageDaters', { id: user_id })" class="nav-item">
          <span class="material-symbols-outlined">favorite</span>
          Manage Daters
        </button>
        
        <button @click="navigateTo('ManageCupids', { id: user_id })" class="nav-item">
          <span class="material-symbols-outlined">person</span>
          Manage Cupids
        </button>
        
        <div class="accessibility-section">
          <h4>Accessibility</h4>
          <button class="nav-item accessibility-toggle" @click="toggleLightMode">
            <span class="material-symbols-outlined">{{ theme === 'light' ? 'dark_mode' : 'light_mode' }}</span>
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
  background-color: var(--new-background);
  border-top: 2px solid var(--new-light-blue);
  border-bottom: 2px solid var(--new-light-blue);
  display: flex;
  align-items: center;
  padding: 0 16px;
  z-index: 1000;
}

.hamburger-btn {
  background: none;
  border: none;
  color: var(--new-primary);
  font-size: 24px;
  cursor: pointer;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hamburger-btn:hover {
  color: var(--new-light-blue);
}

.logo {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  color: var(--new-primary);
  font-size: 18px;
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
  background-color: var(--new-background);
  border-right: 2px solid var(--new-light-blue);
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
  color: var(--new-primary);
  margin: 0;
  font-size: 16px;
}

.close-btn {
  background: none;
  border: none;
  color: var(--new-primary);
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
  color: var(--new-primary);
  font-size: 16px;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s ease;
}

.nav-item:hover {
  background-color: var(--new-secondary);
  color: var(--new-light-blue);
}

.nav-item .material-symbols-outlined {
  font-size: 20px;
}

/* Logout Section */
.logout-section {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid var(--new-accent);
}

.logout-btn {
  color: var(--new-accent) !important;
  font-weight: bold;
}

.logout-btn:hover {
  background-color: var(--new-accent) !important;
  color: var(--new-background) !important;
}

.accessibility-section {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid var(--new-light-blue);
}

.accessibility-section h4 {
  color: var(--new-primary);
  margin: 0 0 12px 16px;
  font-size: 14px;
}

.accessibility-toggle {
  font-style: italic;
}
</style>
