<script setup>
import {ref, computed} from 'vue';
import router from '../router/index.js'
import { makeRequest } from '../utils/make_request';

import Banner from '../components/Banner.vue';
import NavBar from '../components/NavBar.vue';

const user_id  = parseInt(window.location.hash.split('/')[3])

// Form data
const item = ref('')
const budget = ref('')
const sameAsPickup = ref(false)
const pickupAddress = ref({
  street: '',
  apt: '',
  city: '',
  state: '',
  zipCode: ''
})
const dropoffAddress = ref({
  street: '',
  apt: '',
  city: '',
  state: '',
  zipCode: ''
})

// Computed properties to combine address fields into single strings for backend
const pickupLocationString = computed(() => {
  const addr = pickupAddress.value
  const parts = [
    addr.street,
    addr.apt,
    addr.city,
    addr.state,
    addr.zipCode
  ].filter(part => part && part.trim() !== '')
  
  return parts.join(', ')
})

const dropoffLocationString = computed(() => {
  const addr = dropoffAddress.value
  const parts = [
    addr.street,
    addr.apt,
    addr.city,
    addr.state,
    addr.zipCode
  ].filter(part => part && part.trim() !== '')
  
  return parts.join(', ')
})

// Function to copy pickup address to dropoff when checkbox is checked
function handleSameAsPickup() {
  if (sameAsPickup.value) {
    dropoffAddress.value = { ...pickupAddress.value }
  } else {
    // Clear dropoff address when unchecked
    dropoffAddress.value = {
      street: '',
      apt: '',
      city: '',
      state: '',
      zipCode: ''
    }
  }
}

// Form validation
function validateForm() {
  return item.value.trim() !== '' && 
         pickupLocationString.value.trim() !== '' && 
         dropoffLocationString.value.trim() !== ''
}

// Submit function
async function submitGig() {
  if (!validateForm()) {
    alert('Please fill in all required fields')
    return
  }
  
  const gigData = {
    budget: parseFloat(budget.value),
    items_requested: item.value,
    pickup_location: pickupLocationString.value,
    dropoff_location: dropoffLocationString.value
  }
  
  try {
    console.log('Submitting gig:', gigData)
    const response = await makeRequest('/api/gig/create/', 'post', gigData)
    
    if (response) {
      alert('Gig created successfully!')
      // Navigate to DaterGigs page
      router.push({ name: 'DaterGigs', params: { id: user_id } })
    }
  } catch (error) {
    console.error('Error creating gig:', error)
    alert('Failed to create gig. Please try again.')
  }
}

</script>

<template>
    <Banner />
    <NavBar currentPage="CreateGig" />
    
    <div class="container">
        <h1>Create Gig</h1>
        <form class="gig-form">
            <label class="form-field">
                Item
                <input type="text" v-model="item" required>
            </label>

            <!-- Pickup Address Section -->
            <div class="address-section">
                <h3>Pickup Address</h3>
                
                <div class="street-row">
                    <label class="form-field flex-grow">
                        Street Address
                        <input type="text" v-model="pickupAddress.street" required>
                    </label>
                    
                    <label class="form-field apt-field">
                        APT/Unit (Optional)
                        <input type="text" v-model="pickupAddress.apt">
                    </label>
                </div>

                <div class="city-state-row">
                    <label class="form-field flex-grow">
                        City
                        <input type="text" v-model="pickupAddress.city" required>
                    </label>
                    
                    <label class="form-field state-field">
                        State
                        <input type="text" v-model="pickupAddress.state" required>
                    </label>
                </div>

                <label class="form-field">
                    Zip Code
                    <input type="text" v-model="pickupAddress.zipCode" required>
                </label>
            </div>

            <!-- Drop-off Address Section -->
            <div class="address-section">
                <h3>Drop-off Address</h3>
                
                <!-- Same as pickup checkbox -->
                <label class="checkbox-field">
                    <input 
                        type="checkbox" 
                        v-model="sameAsPickup" 
                        @change="handleSameAsPickup"
                        class="checkbox-input"
                    >
                    <span class="checkbox-text">Same as pickup address</span>
                </label>
                
                <div class="street-row">
                    <label class="form-field flex-grow">
                        Street Address
                        <input 
                            type="text" 
                            v-model="dropoffAddress.street" 
                            :disabled="sameAsPickup"
                            required
                        >
                    </label>
                    
                    <label class="form-field apt-field">
                        APT/Unit (Optional)
                        <input 
                            type="text" 
                            v-model="dropoffAddress.apt"
                            :disabled="sameAsPickup"
                        >
                    </label>
                </div>

                <div class="city-state-row">
                    <label class="form-field flex-grow">
                        City
                        <input 
                            type="text" 
                            v-model="dropoffAddress.city" 
                            :disabled="sameAsPickup"
                            required
                        >
                    </label>
                    
                    <label class="form-field state-field">
                        State
                        <input 
                            type="text" 
                            v-model="dropoffAddress.state" 
                            :disabled="sameAsPickup"
                            required
                        >
                    </label>
                </div>

                <label class="form-field">
                    Zip Code
                    <input 
                        type="text" 
                        v-model="dropoffAddress.zipCode" 
                        :disabled="sameAsPickup"
                        required
                    >
                </label>
            </div>

            <label class="form-field">
                Budget ($)
                <input type="number" v-model="budget" required>
            </label>

            <button type="button" @click="submitGig" class="submit-btn">Create Gig</button>
        </form>
    </div>
</template>

<style scoped>
  /* New color scheme variables for testing */
  .container {
    --new-primary: #09A129;     /* Green for text */
    --new-secondary: #1F487E;   /* Dark blue for buttons */
    --new-background: #000000;  /* Black for backgrounds */
    --new-accent: #FB3640;      /* Red (not used here) */
    --new-light-blue: #00CCFF;  /* Light blue (not used here) */
    
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    background-color: var(--new-background);
    min-height: 100vh;
    
    /* Fixed spacing for Banner and NavBar */
    padding-top: 80px; /* Space for banner + navbar + gap */
  }

  /* Mobile: Add bottom margin for bottom navbar */
  @media (max-width: 768px) {
    .container {
      padding-top: 60px; /* Space for banner + extra spacing on mobile */
      padding-bottom: 140px; /* Space for bottom navbar */
    }
  }

  /* Desktop: Add top margin for navbar below banner */
  @media (min-width: 769px) {
    .container {
      padding-top: 160px; /* Space for banner + navbar + gaps */
    }
  }

  .gig-form {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 500px;
    gap: 20px;
  }

  .form-field {
    display: flex;
    flex-direction: column;
    gap: 5px;
    font-weight: bold;
    color: var(--new-primary);
  }

  .form-field input {
    padding: 10px;
    border: 1px solid var(--new-primary);
    border-radius: 4px;
    font-size: 16px;
    background-color: var(--new-background);
    color: var(--new-primary);
  }

  .form-field input:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    background-color: rgba(31, 72, 126, 0.2);
  }

  /* Checkbox styling */
  .checkbox-field {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 15px;
    font-weight: bold;
    color: var(--new-primary);
    cursor: pointer;
  }

  .checkbox-input {
    width: 18px;
    height: 18px;
    accent-color: var(--new-primary);
    cursor: pointer;
    background-color: var(--new-background);
    border: 2px solid var(--new-primary);
    border-radius: 3px;
    appearance: none;
    position: relative;
  }

  .checkbox-input:checked {
    background-color: var(--new-primary);
  }

  .checkbox-input:checked::after {
    content: '✓';
    position: absolute;
    top: -2px;
    left: 2px;
    color: var(--new-background);
    font-size: 14px;
    font-weight: bold;
  }

  .checkbox-text {
    font-size: 16px;
    user-select: none;
  }

  .form-field input:focus {
    outline: 2px solid var(--new-primary);
    border-color: var(--new-primary);
  }

  .address-section {
    border: 1px solid var(--new-primary);
    border-radius: 8px;
    padding: 15px;
    background-color: var(--new-background);
  }

  .address-section h3 {
    margin: 0 0 15px 0;
    color: var(--new-primary);
  }

  .street-row {
    display: flex;
    gap: 10px;
    margin-bottom: 15px;
  }

  .city-state-row {
    display: flex;
    gap: 10px;
    margin-bottom: 15px;
  }

  .flex-grow {
    flex: 1;
    min-width: 0; /* Allow flex items to shrink below their content size */
  }

  .apt-field {
    flex: 0 0 120px;
    max-width: 120px;
    min-width: 80px;
  }

  .state-field {
    flex: 0 0 80px;
    max-width: 80px;
    min-width: 60px;
  }

  /* Responsive adjustments for smaller screens */
  @media (max-width: 480px) {
    .apt-field {
      flex: 0 0 90px;
      max-width: 90px;
    }
    
    .state-field {
      flex: 0 0 70px;
      max-width: 70px;
    }
    
    .street-row,
    .city-state-row {
      gap: 8px;
    }
  }

  .submit-btn {
    padding: 12px 24px;
    background-color: var(--new-secondary);
    color: var(--new-primary);
    border: 1px solid var(--new-primary);
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
    margin-top: 10px;
    font-weight: bold;
  }

  .submit-btn:hover {
    background-color: var(--new-primary);
    color: var(--new-background);
  }

  h1 {
    text-align: center;
    margin-bottom: 20px;
    color: var(--new-primary);
  }
</style>