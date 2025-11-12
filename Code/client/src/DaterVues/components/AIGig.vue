<script setup>
import { ref, computed } from 'vue'
import { makeRequest } from '../../utils/make_request'
import { loadScript } from '@paypal/paypal-js'
import GigMap from '../../CupidVues/GigMap.vue'

const props = defineProps({
  gigData: {
    type: Object,
    required: true
  },
  userId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['close', 'gigCreated'])

const showPayPal = ref(false)
const paypalLoaded = ref(false)
const showMap = ref(false)
const isCreating = ref(false)
const editableBudget = ref('')

// PayPal integration
const previewTotalCost = computed(() => {
  const budget = parseFloat(editableBudget.value)
  if (isNaN(budget) || budget <= 0) return '$0.00'
  const fee = budget * 0.10
  const total = budget + fee
  return `$${total.toFixed(2)}`
})

const totalCostValue = computed(() => {
  const budget = parseFloat(editableBudget.value)
  if (isNaN(budget) || budget <= 0) return 0
  return (budget + (budget * 0.10)).toFixed(2)
})

// Initialize PayPal
async function initializePayPal() {
  try {
    const config = await makeRequest('/api/paypal/config/')
    if (!config?.CLIENT_ID) return false
    
    const paypal = await loadScript({
      clientId: config.CLIENT_ID,
      currency: config.CURRENCY || 'USD'
    })
    
    return !!paypal
  } catch (error) {
    console.error('Failed to load PayPal:', error)
    return false
  }
}

async function acceptGig() {
  showPayPal.value = true
  paypalLoaded.value = await initializePayPal()
  
  if (paypalLoaded.value) {
    setTimeout(renderPayPalButtons, 100)
  } else {
    alert('Failed to load PayPal. Please try again.')
    showPayPal.value = false
  }
}

function renderPayPalButtons() {
  const container = document.getElementById('ai-gig-paypal-container')
  if (!container) return
  
  container.innerHTML = ''
  
  window.paypal.Buttons({
    createOrder: (data, actions) => {
      return actions.order.create({
        purchase_units: [{
          amount: { value: totalCostValue.value },
          description: `Cupid Gig: ${props.gigData.keyword} from ${props.gigData.place_name}`
        }]
      })
    },
    onApprove: async (data, actions) => {
      const order = await actions.order.capture()
      await createGigAfterPayment(order.id)
    },
    onError: () => {
      alert('Payment failed. Please try again.')
      showPayPal.value = false
    },
    onCancel: () => {
      showPayPal.value = false
    }
  }).render('#ai-gig-paypal-container')
}

async function createGigAfterPayment(paypalOrderId) {
  try {
    isCreating.value = true
    
    const gigData = {
      budget: parseFloat(editableBudget.value),
      items_requested: props.gigData.keyword,
      pickup_location: props.gigData.pickup_location,
      dropoff_location: props.gigData.dropoff_location,
      payment_id: paypalOrderId
    }
    
    const response = await makeRequest('/api/gig/create/', 'post', gigData)
    if (response) {
      emit('gigCreated', response)
      emit('close')
    }
  } catch (error) {
    console.error('Error creating gig:', error)
    alert('Failed to create gig. Please try again.')
  } finally {
    isCreating.value = false
  }
}

async function openMap() {
  // Ensure we have user location before opening map
  if (!props.gigData.dropoff_location) {
    try {
      const position = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, {
          enableHighAccuracy: true,
          timeout: 5000
        })
      })
      
      props.gigData.dropoff_location = `${position.coords.latitude},${position.coords.longitude}`
    } catch (error) {
      console.warn('Could not get location for map:', error)
    }
  }
  showMap.value = true
}

function closeMap() {
  showMap.value = false
}

function decline() {
  emit('close')
}
</script>

<template>
  <div class="ai-gig-overlay">
    <div class="ai-gig-container">
      <!-- Header -->
      <div class="gig-header">
        <h2>🤖 AI Found a Gig for You!</h2>
        <button @click="decline" class="close-btn">&times;</button>
      </div>
      
      <!-- Gig Details -->
      <div class="gig-content" v-if="!showPayPal">
        <div class="place-info">
          <div class="place-header">
            <h3>{{ gigData.place_name }}</h3>
            <div v-if="gigData.place_rating" class="rating">
              ⭐ {{ gigData.place_rating }}
            </div>
          </div>
          
          <div class="place-details">
            <p><strong>Item:</strong> {{ gigData.keyword }}</p>
            <p><strong>Pickup:</strong> {{ gigData.pickup_location }}</p>
            
            <!-- Editable Budget Field -->
            <div class="budget-field">
              <label for="budget-input"><strong>Budget ($):</strong></label>
              <input 
                id="budget-input"
                type="number" 
                v-model="editableBudget" 
                min="1" 
                step="0.01"
                class="budget-input"
                placeholder="Enter amount"
              />
            </div>
            
            <p><strong>Total Cost:</strong> {{ previewTotalCost }}</p>
          </div>
          
          <div v-if="gigData.place_photo_url" class="place-photo">
            <img :src="gigData.place_photo_url" :alt="gigData.place_name" />
          </div>
        </div>
        
        <!-- Action Buttons -->
        <div class="action-buttons">
          <button 
            @click="acceptGig" 
            class="accept-btn"
            :disabled="!editableBudget || parseFloat(editableBudget) <= 0"
            :class="{ disabled: !editableBudget || parseFloat(editableBudget) <= 0 }"
          >
            💳 Accept & Pay
          </button>
          <button @click="openMap" class="map-btn">
            🗺️ View Map
          </button>
          <button @click="decline" class="decline-btn">
            ❌ Decline
          </button>
        </div>
      </div>
      
      <!-- PayPal Payment -->
      <div v-if="showPayPal" class="payment-section">
        <h3>Complete Payment</h3>
        <p>Total: {{ previewTotalCost }}</p>
        <div id="ai-gig-paypal-container"></div>
        <button @click="showPayPal = false" class="cancel-payment-btn">Cancel</button>
      </div>
    </div>
    
    <!-- Map Modal -->
    <GigMap 
      v-if="showMap"
      :pickup-location="gigData.pickup_coords ? `${gigData.pickup_coords.lat},${gigData.pickup_coords.lng}` : gigData.pickup_location"
      :dropoff-location="gigData.dropoff_location"
      :gig-title="`${gigData.keyword} at ${gigData.place_name}`"
      :cupid-id="userId"
      @close="closeMap"
    />
  </div>
</template>

<style scoped>
.ai-gig-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1500;
  padding: 20px;
}

.budget-field {
  margin: 10px 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.budget-field label {
  color: #09A129;
  font-weight: bold;
}

.accept-btn.disabled {
  background-color: #666666;
  color: #999999;
  cursor: not-allowed;
  opacity: 0.5;
}

.accept-btn:disabled {
  background-color: #666666;
  color: #999999;
  cursor: not-allowed;
  opacity: 0.5;
}

.budget-input {
  padding: 8px 12px;
  border: 2px solid #09A129;
  border-radius: 4px;
  background-color: #000000;
  color: #09A129;
  font-size: 16px;
  width: 100px;
}

.budget-input:focus {
  outline: none;
  border-color: #00CCFF;
}

.ai-gig-container {
  background-color: #000000;
  border: 2px solid #09A129;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.gig-header {
  background-color: #1F487E;
  color: #09A129;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #09A129;
}

.gig-header h2 {
  margin: 0;
  font-size: 1.4em;
}

.close-btn {
  background: none;
  border: none;
  color: #09A129;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.gig-content {
  padding: 20px;
}

.place-info {
  margin-bottom: 20px;
}

.place-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.place-header h3 {
  color: #09A129;
  margin: 0;
}

.rating {
  color: #00CCFF;
  font-weight: bold;
}

.place-details {
  color: #09A129;
  margin-bottom: 15px;
}

.place-details p {
  margin: 8px 0;
}

.place-photo img {
  width: 100%;
  max-height: 200px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #09A129;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.accept-btn {
  background-color: #09A129;
  color: #000000;
  border: none;
  padding: 15px;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  font-size: 16px;
}

.map-btn {
  background-color: #00CCFF;
  color: #000000;
  border: none;
  padding: 12px;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}

.decline-btn {
  background-color: #FB3640;
  color: #ffffff;
  border: none;
  padding: 12px;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}

.payment-section {
  padding: 20px;
  text-align: center;
}

.payment-section h3 {
  color: #09A129;
  margin-bottom: 10px;
}

.payment-section p {
  color: #09A129;
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
}

.cancel-payment-btn {
  background-color: #FB3640;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}
</style>