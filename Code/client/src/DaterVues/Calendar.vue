<script setup>
import { makeRequest } from '../utils/make_request';
import {onMounted, ref, computed} from 'vue';
import Banner from '../components/Banner.vue';
import NavBar from '../components/NavBar.vue';
import router from '../router';

const user_id = router.currentRoute.value.params.id

const newDate = ref('')
const address = ref({
  street: '',
  apt: '',
  city: '',
  state: '',
  zipCode: ''
})
const desc = ref('')
const budget = ref(0.0)

// Computed property to combine address fields into single string for backend
const locationString = computed(() => {
  const addr = address.value
  const parts = [
    addr.street,
    addr.apt,
    addr.city,
    addr.state,
    addr.zipCode
  ].filter(part => part && part.trim() !== '')
  
  return parts.join(', ')
})

async function getCalendar() {
  const results = await makeRequest(`/api/dater/calendar/${user_id}/`);
  const dates = document.getElementById('dates')
  console.log(results)
  // put calendar to screen
  for (let res of results) {
    const date = document.createElement('div')
    date.setAttribute('class', 'date')
    date.setAttribute('id', res.id)
    date.innerHTML = `
      <h3>${res.date_time.split('T')[0]}</h3>
      <span>${res.location}</span>
      <span>${res.description}</span>
      <span >${res.status}</span>
    `
    const button = document.createElement('button')
    button.setAttribute('class', "button")
    button.setAttribute('onclick', `${() => {
      if (res.status === 'planned') res.status = 'completed'
      else res.status = 'planned'
    } }`)
    button.innerText = 'Change Status'
    date.appendChild(button)
    dates.appendChild(date)
  }
}

async function addDate() {
  console.log(newDate.value)
  // Add to screen
  const dates = document.getElementById('dates')

  const res = await makeRequest(`/api/dater/calendar/${user_id}/`, 'post', {
    date_time: newDate.value,
    location: locationString.value,
    description: desc.value,
    status: 'planned',
    budget: budget.value,
  })

  const date = document.createElement('div')
  date.setAttribute('class', 'date')
  date.setAttribute('id', res.id)
  date.innerHTML = `
    <h3>${res.date_time.split('T')[0]}</h3>
    <span>${res.location}</span>
    <span>${res.status}</span>
  `
  const button = document.createElement('button')
  button.setAttribute('class', "button")
  button.setAttribute('onclick', `${() => {
    if (res.status === 'planned') res.status = 'completed'
    else res.status = 'planned'
  } }`)
  button.innerText = 'Change Status'
  date.appendChild(button)
  dates.appendChild(date)
}

onMounted(() => getCalendar())
</script>

<template>  
    <Banner />
    <NavBar currentPage="Calendar" />

    <main>
        <!-- Fixed Header Bar -->
        <div class="header-bar">
            <h1 class="page-title">Calendar</h1>
        </div>

        <div class="container">
            <div class="header">
                <h2>View Upcoming Dates and Add New Dates!</h2>
                <form class="form" @submit.prevent="addDate">
                    <label for="date">Choose the Day</label>
                    <input type="date" class="add-date" id="date" v-model="newDate">
                    
                    <!-- Address Section -->
                    <div class="address-section">
                        <h3>Where are you Going?</h3>
                        
                        <div class="street-row">
                            <label class="form-field flex-grow">
                                Street Address
                                <input type="text" v-model="address.street" class="add-date" required>
                            </label>
                            
                            <label class="form-field apt-field">
                                APT/Unit (Optional)
                                <input type="text" v-model="address.apt" class="add-date">
                            </label>
                        </div>

                        <div class="city-state-row">
                            <label class="form-field flex-grow">
                                City
                                <input type="text" v-model="address.city" class="add-date" required>
                            </label>
                            
                            <label class="form-field state-field">
                                State
                                <input type="text" v-model="address.state" class="add-date" required>
                            </label>
                        </div>

                        <label class="form-field">
                            Zip Code
                            <input type="text" v-model="address.zipCode" class="add-date" required>
                        </label>
                    </div>
                    
                    <label for="desc">What will you be doing?</label>
                    <input type="text" class="add-date" id="desc" v-model="desc" placeholder="Describe your date...">
                    
                    <label for="budget">Max budget for Gigs ($XX.XX)</label>
                    <input type="number" class="add-date" id="budget" v-model="budget" step="0.01" min="0" placeholder="0.00">
                    
                    <button type="submit" class="add-button">
                        <span class="material-symbols-outlined">add</span>
                        Add Date
                    </button>
                </form>
            </div>

            <div class="dates" id="dates"></div>
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
    margin-top: 60px; /* Space for banner */
    padding-bottom: 120px;
}

/* Mobile: Add bottom padding for bottom navbar */
@media (max-width: 768px) {
    main {
        padding-bottom: 160px; /* Space for navbar */
    }
}

/* Desktop: Add top margin for navbar below banner */
@media (min-width: 769px) {
    main {
        margin-top: 140px; /* Space for banner + navbar + gaps */
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
    justify-content: center;
    align-items: center;
    z-index: 999;
}

/* Mobile: Position below banner */
@media (max-width: 768px) {
    .header-bar {
        top: 60px; /* Below banner, navbar is at bottom */
    }
}

/* Desktop: Position below banner and navbar */
@media (min-width: 769px) {
    .header-bar {
        top: 140px; /* Below banner + navbar + gaps */
        border-top: 2px solid var(--new-primary);
    }
}

.page-title {
    color: var(--new-primary);
    margin: 0;
    font-size: 2.2em;
    font-weight: bold;
}

@media (max-width: 600px) {
    .page-title {
        font-size: 1.8em;
    }
}

.container {
    flex: 1;
    padding: 20px;
    margin-top: 80px; /* Space for header bar */
}

@media (max-width: 768px) {
    .container {
        margin-top: 60px; /* Adjusted for mobile */
        padding: 12px;
    }
}

.header {
    display: flex;
    flex-direction: column;
    align-items: center;
    border-bottom: 3px solid var(--new-primary);
    margin-bottom: 30px;
    padding-bottom: 20px;
}

.header h2 {
    margin: 8px 0 20px 0;
    color: var(--new-primary);
    text-align: center;
    font-size: 1.4em;
}

.form {
    display: flex;
    flex-direction: column;
    gap: 16px;
    width: 100%;
    max-width: 400px;
    margin: 0 auto;
}

.form label {
    color: var(--new-primary);
    font-weight: bold;
    margin-bottom: 4px;
    text-align: left;
}

.add-date {
    border: 2px solid var(--new-primary);
    border-radius: 8px;
    padding: 12px 16px;
    background-color: var(--new-background);
    color: var(--new-primary);
    font-size: 16px;
    outline: none;
    transition: all 0.3s ease;
}

/* Special styling for date input to make calendar button visible */
.add-date[type="date"] {
    position: relative;
    color-scheme: dark;
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%2309A129'%3e%3cpath d='M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z'/%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right 12px center;
    background-size: 20px 20px;
    padding-right: 40px;
}

.add-date[type="date"]::-webkit-calendar-picker-indicator {
    background: transparent;
    bottom: 0;
    color: transparent;
    cursor: pointer;
    height: auto;
    left: 0;
    position: absolute;
    right: 0;
    top: 0;
    width: auto;
    opacity: 0;
}

/* Firefox date input styling */
.add-date[type="date"]::-moz-calendar-picker-indicator {
    filter: invert(39%) sepia(89%) saturate(1000%) hue-rotate(90deg) brightness(95%) contrast(95%);
    cursor: pointer;
}

.add-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background-color: var(--new-secondary);
    border: 2px solid var(--new-primary);
    border-radius: 8px;
    padding: 12px 20px;
    color: var(--new-primary);
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 8px;
}

.add-button:hover {
    background-color: var(--new-primary);
    color: var(--new-background);
    transform: translateY(-1px);
}

.add-button .material-symbols-outlined {
    font-size: 20px;
}

.dates {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

/* Style for dynamically created date cards */
:global(.date) {
    background-color: var(--new-secondary);
    border: 2px solid var(--new-primary);
    border-radius: 12px;
    padding: 16px;
    color: var(--new-primary);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
}

:global(.date:hover) {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
}

:global(.date h3) {
    margin: 0 0 12px 0;
    color: var(--new-light-blue);
    font-size: 1.2em;
    border-bottom: 1px solid var(--new-primary);
    padding-bottom: 8px;
}

:global(.date span) {
    display: block;
    margin: 8px 0;
    line-height: 1.4;
}

:global(.date .button) {
    background-color: var(--new-accent);
    border: 2px solid var(--new-accent);
    border-radius: 6px;
    padding: 8px 16px;
    color: white;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 12px;
    width: 100%;
}

:global(.date .button:hover) {
    background-color: white;
    color: var(--new-accent);
    transform: translateY(-1px);
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .dates {
        grid-template-columns: 1fr;
        gap: 16px;
    }
    
    .form {
        max-width: 100%;
    }
}

.address-section {
    border: 2px solid var(--new-primary);
    border-radius: 8px;
    padding: 16px;
    background-color: var(--new-background);
    margin: 16px 0;
}

.address-section h3 {
    margin: 0 0 16px 0;
    color: var(--new-primary);
    font-size: 1.1em;
}

.street-row {
    display: flex;
    gap: 12px;
    margin-bottom: 16px;
}

.city-state-row {
    display: flex;
    gap: 12px;
    margin-bottom: 16px;
}

.form-field {
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-weight: bold;
    color: var(--new-primary);
}

.flex-grow {
    flex: 1;
    min-width: 0;
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
    
    .address-section {
        padding: 12px;
    }
}
</style>
