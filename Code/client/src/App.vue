<script setup>
import { ref, onMounted, computed, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import router from './router/index.js';
import { makeRequest } from './utils/make_request.js';
import Popup from './components/Popup.vue'

const popupActive = ref(false)
const route = useRoute()
const currentNotification = ref(null)
const isPolling = ref(false)
const lastCheck = ref(new Date().toISOString())
const user_id = ref(null)

const isNotLoginPage = computed(() => {
  return route.path !== '/' && route.path !== '/login'
})

async function getUser() {
  const results = await makeRequest('api/user/', 'get', {
    user_id: user_id
  })
}

function updateUserId() {
  const id = parseInt(window.location.hash.split('/')[3]);
  if (!isNaN(id) && id > 0) {
    user_id.value = id;
  } else {
    user_id.value = null;
  }
}

// Long polling for notifications
async function startNotificationPolling() {
  if (isPolling.value) return;
  if (!user_id.value) return;
  
  console.log(`Starting notification polling for user ${user_id.value}`);
  isPolling.value = true;
  
  while (isPolling.value) {
    try {
      const response = await makeRequest(
        `api/notifications/${user_id.value}/?last_check=${encodeURIComponent(lastCheck.value)}&timeout=30`, 
        'get'
      );
      
      // Update last check time
      lastCheck.value = response.current_time;
      
      // Show notifications
      if (response.notifications && response.notifications.length > 0) {
        response.notifications.forEach(notification => {
          notify(notification);
        });
      }
      
      // If timed out, wait a bit before next poll
      if (response.timeout) {
        await sleep(3000);
      }
      
    } catch (error) {
      console.error('Notification polling error:', error);
      await sleep(5000); // Wait on error
    }
  }
}

async function notify(notification) {
  currentNotification.value = notification;
  popupActive.value = true;

  setTimeout(() => {
    popupActive.value = false;
    currentNotification.value = null;
  }, 5000);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function hideNotification() {
  popupActive.value = false;
  currentNotification.value = null;
}

watch(() => route.path, () => {
  updateUserId();
});

watch(user_id, (newId, oldId) => {
  if (newId && newId !== oldId) {
    isPolling.value = false;
    lastCheck.value = new Date().toISOString();
    setTimeout(() => startNotificationPolling(), 100);
  } else if (!newId && isPolling.value) {
    isPolling.value = false;
  }
});

onMounted(() => {
  updateUserId();
});

onUnmounted(() => {
  isPolling.value = false;
});

// Stop polling when user navigates away or closes tab
window.addEventListener('beforeunload', () => {
  isPolling.value = false;
});
</script>

<template>
  <div id="app">
    <!-- Remove the manual toggle button, notifications will appear automatically -->
    
    <Popup v-if="isNotLoginPage && popupActive" :data-active="popupActive ? 'true' : 'false'">
      <div class="notification-content" @click="hideNotification">
        <div class="notification-icon" aria-hidden="true">
          <span class="material-symbols-outlined" v-if="currentNotification?.type === 'feedback'">star</span>
          <span class="material-symbols-outlined" v-else-if="currentNotification?.type === 'gig_claimed'">handshake</span>
          <span class="material-symbols-outlined" v-else-if="currentNotification?.type === 'gig_completed'">check_circle</span>
          <span class="material-symbols-outlined" v-else-if="currentNotification?.type === 'gig_dropped'">cancel</span>
          <span class="material-symbols-outlined" v-else>notifications</span>
        </div>
        <p>{{ currentNotification?.message || 'New notification!' }}</p>
        <button class="notification-close" @click.stop="hideNotification">&times;</button>
      </div>
    </Popup>
  </div>
  <router-view />
</template>

<style scoped>
  .notification-content {
    /* Color scheme variables - same as DaterHome */
    --new-primary: #09A129;     /* Green for text */
    --new-secondary: #1F487E;   /* Dark blue for buttons */
    --new-background: #000000;  /* Black for backgrounds */
    --new-accent: #FB3640;      /* Red */
    --new-light-blue: #00CCFF;  /* Light blue */
    
    padding: 16px;
    border-radius: 8px;
    background: rgba(255,255,255,0.08);
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    position: relative;
    cursor: pointer;
    border: 2px solid var(--new-primary);
  }
  
  .notification-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 8px;
    color: var(--new-primary);
  }
  
  .notification-icon .material-symbols-outlined {
    font-size: 28px;
    line-height: 1;
  }
  
  .notification-content p {
    margin: 0;
    font-size: 16px;
    color: var(--new-primary);
  }
  
  .notification-close {
    position: absolute;
    top: 5px;
    right: 10px;
    background: none;
    border: none;
    color: var(--new-primary);
    font-size: 20px;
    cursor: pointer;
    opacity: 0.7;
  }
  
  .notification-close:hover {
    opacity: 1;
    color: var(--new-light-blue);
  }
</style>
