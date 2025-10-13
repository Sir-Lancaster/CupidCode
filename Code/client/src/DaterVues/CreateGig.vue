<script setup>
import {ref, computed} from 'vue';
import router from '../router/index.js'
import { makeRequest } from '../utils/make_request';

import Banner from '../components/Banner.vue';
import NavBar from '../components/NavBar.vue';

const user_id  = parseInt(window.location.hash.split('/')[3])

// Form data
const date = ref('')
const item = ref('')
const budget = ref('')
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

</script>

<template>
    <Banner />
    <NavBar currentPage="CreateGig" />
    
    <div class="container">
        <h1>Create Gig</h1>
        <form class="gig-form">
            <label class="form-field">
                Date
                <input type="date" v-model="date" required>
            </label>

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
                
                <div class="street-row">
                    <label class="form-field flex-grow">
                        Street Address
                        <input type="text" v-model="dropoffAddress.street" required>
                    </label>
                    
                    <label class="form-field apt-field">
                        APT/Unit (Optional)
                        <input type="text" v-model="dropoffAddress.apt">
                    </label>
                </div>

                <div class="city-state-row">
                    <label class="form-field flex-grow">
                        City
                        <input type="text" v-model="dropoffAddress.city" required>
                    </label>
                    
                    <label class="form-field state-field">
                        State
                        <input type="text" v-model="dropoffAddress.state" required>
                    </label>
                </div>

                <label class="form-field">
                    Zip Code
                    <input type="text" v-model="dropoffAddress.zipCode" required>
                </label>
            </div>

            <label class="form-field">
                Budget ($)
                <input type="number" v-model="budget" required>
            </label>

            <button type="submit" class="submit-btn">Create Gig</button>
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
    
    /* Spacing for Banner and NavBar */
    margin-top: 60px; /* Space for banner (60px) + gap */
  }

  /* Mobile: Add bottom margin for bottom navbar */
  @media (max-width: 768px) {
    .container {
      margin-bottom: 90px; /* Space for bottom navbar */
    }
  }

  /* Desktop: Add top margin for navbar below banner */
  @media (min-width: 769px) {
    .container {
      margin-top: 140px; /* Space for banner + navbar + gaps */
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