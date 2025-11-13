<script setup>
import { ref, onMounted, computed, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import router from './router/index.js';
import { makeRequest } from './utils/make_request.js';
import Popup from './components/Popup.vue'

// Debug helper so all logs are easy to filter in the browser console
const debug = (...args) => console.log('[NOTIF]', ...args)

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
  const before = user_id.value
  if (!isNaN(id) && id > 0) {
    user_id.value = id;
    debug('updateUserId -> valid user_id detected', { route: route.path, parsedId: id, previous: before, current: user_id.value })
  } else {
    debug('updateUserId -> no valid user_id found', { route: route.path, parsedId: id, previous: before })
    user_id.value = null;
  }
}

// Long polling for notifications
async function startNotificationPolling() {
  if (isPolling.value) {
    debug('startNotificationPolling called but polling already active')
    return;
  }
  if (!user_id.value) {
    debug('startNotificationPolling aborted: no user_id')
    return;
  }
  
  debug('Starting notification polling', { user: user_id.value, lastCheck: lastCheck.value })
  isPolling.value = true;
  
  while (isPolling.value) {
    try {
      const url = `api/notifications/${user_id.value}/?last_check=${encodeURIComponent(lastCheck.value)}&timeout=30`;
      debug('Polling request', { url, lastCheck: lastCheck.value })
      const response = await makeRequest(url, 'get');
      
      // Update last check time
      const prevLast = lastCheck.value;
      lastCheck.value = response.current_time;
      debug('Polling response', { timeout: !!response.timeout, notifications: (response.notifications || []).length, current_time: response.current_time })
      debug('Updated lastCheck', { from: prevLast, to: lastCheck.value })
      
      // Show notifications
      if (response.notifications && response.notifications.length > 0) {
        response.notifications.forEach(notification => {
          debug('Showing notification', { type: notification?.type, timestamp: notification?.timestamp, message: notification?.message })
          notify(notification);
        });
      } else {
        debug('No notifications this cycle')
      }
      
      // If timed out, wait a bit before next poll
      if (response.timeout) {
        debug('Server long-poll timeout: sleeping 3000ms before next poll')
        await sleep(3000);
      }
      
    } catch (error) {
      console.error('[NOTIF] Notification polling error:', error);
      debug('Sleeping 5000ms after error')
      await sleep(5000); // Wait on error
    }
  }

  debug('Polling loop exited (isPolling is false)')
}

async function notify(notification) {
  debug('notify()', { notification })
  currentNotification.value = notification;
  popupActive.value = true;

  setTimeout(() => {
    debug('Auto-hide notification after 5s')
    popupActive.value = false;
    currentNotification.value = null;
  }, 5000);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function hideNotification() {
  debug('hideNotification() called by user')
  popupActive.value = false;
  currentNotification.value = null;
}

watch(() => route.path, () => {
  debug('Route changed', { path: route.path, hash: window.location.hash })
  updateUserId();
});

watch(user_id, (newId, oldId) => {
  if (newId && newId !== oldId) {
    debug('user_id changed -> restarting polling', { from: oldId, to: newId })
    if (isPolling.value) {
      debug('Stopping existing polling loop before restart')
    }
    isPolling.value = false;
    lastCheck.value = new Date().toISOString();
    setTimeout(() => startNotificationPolling(), 100);
  } else if (!newId && isPolling.value) {
    debug('user_id cleared -> stopping polling')
    isPolling.value = false;
  }
});

onMounted(() => {
  debug('App mounted')
  updateUserId();
});

onUnmounted(() => {
  debug('App unmounted -> stopping polling')
  isPolling.value = false;
});

// Stop polling when user navigates away or closes tab
window.addEventListener('beforeunload', () => {
  debug('beforeunload -> stopping polling')
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
