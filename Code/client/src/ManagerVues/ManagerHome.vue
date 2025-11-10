<script setup>
import {ref, onMounted, computed} from 'vue'
import { makeRequest } from '../utils/make_request';
import {to_pdf} from '../utils/to_PDF';
import ManagerBanner from './components/ManagerBanner.vue';
import ManagerNavBar from './components/ManagerNavBar.vue';
import router from '../router';

// Use router params instead of hash extraction
const user_id = router.currentRoute.value.params.id

const daters = ref(0)
const cupids = ref(0)
const active_cupids = ref(0)
const active_daters = ref(0)

const gigs = ref(0)
const rate = ref(0)
const dropped = ref(0)
const completed = ref(0)

async function getDatersTotal() {
  try {
    const results = await makeRequest('/api/manager/dater_count/')
    daters.value = results.count
  } catch (error) {
    console.error('Error fetching dater count:', error)
    daters.value = 'Error'
  }
}

async function getCupidsTotal() {
  try {
    const results = await makeRequest('/api/manager/cupid_count/')
    cupids.value = results.count
  } catch (error) {
    console.error('Error fetching cupid count:', error)
    cupids.value = 'Error'
  }
}

async function getCurrActiveTotal() {
  try {
    const cupid_res = await makeRequest('/api/manager/active_cupids/')
    console.log('Cupid response:', cupid_res) // Debug log
    // Handle both formats: {data: number} or just number
    active_cupids.value = cupid_res.data !== undefined ? cupid_res.data : cupid_res
    
    const dater_res = await makeRequest('/api/manager/active_daters/')
    console.log('Dater response:', dater_res) // Debug log
    // Handle both formats: {data: number} or just number
    active_daters.value = dater_res.data !== undefined ? dater_res.data : dater_res
  } catch (error) {
    console.error('Error fetching active users:', error)
    active_cupids.value = 'Error'
    active_daters.value = 'Error'
  }
}

async function getGigData() {
  try {
    // Get gig rate
    const rate_res = await makeRequest('/api/manager/gig_rate/')
    rate.value = rate_res.gig_rate

    // Get total gig count
    const count_res = await makeRequest('/api/manager/gig_count/')
    gigs.value = count_res.count

    // Get completion rate
    const completed_res = await makeRequest('/api/manager/gig_complete_rate/')
    completed.value = completed_res.gig_complete_rate

    // Get drop rate
    const dropped_res = await makeRequest('/api/manager/gig_drop_rate/')
    dropped.value = dropped_res.drop_rate
  } catch (error) {
    console.error('Error fetching gig data:', error)
    rate.value = 'Error'
    gigs.value = 'Error'
    completed.value = 'Error'
    dropped.value = 'Error'
  }
}

function toPDF() {
  const content = document.querySelector('#content')
  to_pdf(content)
}

// Calculate recent activity (last 24 hours) using real data
const recentActivityData = computed(() => {
  const totalGigs = gigs.value || 0
  const completionRate = completed.value || 0
  const gigRatePerHour = rate.value || 0
  const dropRatePerHour = dropped.value || 0
  
  if (totalGigs === 'Error' || gigRatePerHour === 'Error') {
    return []
  }
  
  // Calculate actual numbers for LAST 24 HOURS
  const completedToday = Math.floor(totalGigs * completionRate) // Completed gigs from last 24 hours
  const createdToday = Math.floor(gigRatePerHour * 24) // Gigs created per hour * 24 hours
  const droppedToday = Math.floor(dropRatePerHour * 24) // Drops per hour * 24 hours
  
  return [
    { 
      label: 'Created Today', 
      value: createdToday,
      color: 'var(--new-light-blue)'
    },
    { 
      label: 'Completed Today', 
      value: completedToday,
      color: 'var(--new-primary)'
    },
    { 
      label: 'Dropped Today', 
      value: droppedToday,
      color: 'var(--new-accent)'
    }
  ]
})

const maxValue = computed(() => {
  if (recentActivityData.value.length === 0) return 10
  return Math.max(...recentActivityData.value.map(d => d.value), 5) // Minimum of 5 for scale
})

onMounted(async () => {
  // Enable real API calls
  await getDatersTotal()
  await getCupidsTotal()
  await getCurrActiveTotal()
  await getGigData()
})
</script>

<template>
    <ManagerBanner />
    <ManagerNavBar currentPage="ManagerHome" />

    <main>
        <!-- Fixed Header Bar -->
        <div class="header-bar">
            <h1 class="page-title">Manager Dashboard</h1>
        </div>

        <div class="container">
            <div id="content">
                <!-- Recent Activity Bar Chart -->
                <div class="chart-section">
                    <h3>Recent Activity (Last 24 Hours)</h3>
                    <figure class="graph-container">
                        <div v-if="gigs === 'Error' || rate === 'Error'" class="graph-placeholder">
                            <span class="material-symbols-outlined">bar_chart</span>
                            <p>Activity Data Unavailable</p>
                            <span class="placeholder-subtitle">Error loading recent activity data</span>
                        </div>
                        
                        <div v-else class="bar-chart-container">
                            <svg width="100%" height="300" viewBox="0 0 500 300" class="bar-chart">
                                <!-- Background Grid Lines -->
                                <defs>
                                    <pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse">
                                        <path d="M 50 0 L 0 0 0 50" fill="none" stroke="var(--new-primary)" stroke-width="0.5" opacity="0.3"/>
                                    </pattern>
                                </defs>
                                <rect width="100%" height="100%" fill="url(#grid)" />
                                
                                <!-- Chart Area Background -->
                                <rect x="80" y="30" width="380" height="220" fill="none" stroke="var(--new-primary)" stroke-width="1" opacity="0.5"/>
                                
                                <!-- Y-axis Labels -->
                                <text x="70" y="40" text-anchor="end" fill="var(--new-primary)" font-size="12" font-weight="bold">{{ maxValue }}</text>
                                <text x="70" y="140" text-anchor="end" fill="var(--new-primary)" font-size="12" font-weight="bold">{{ Math.floor(maxValue/2) }}</text>
                                <text x="70" y="240" text-anchor="end" fill="var(--new-primary)" font-size="12" font-weight="bold">0</text>
                                
                                <!-- Bars -->
                                <rect 
                                    v-for="(item, index) in recentActivityData"
                                    :key="item.label"
                                    :x="100 + index * 120"
                                    :y="250 - (item.value / maxValue * 220)"
                                    width="80"
                                    :height="(item.value / maxValue * 220)"
                                    :fill="item.color"
                                    stroke="var(--new-background)"
                                    stroke-width="2"
                                    class="bar"
                                    rx="4"
                                />
                                
                                <!-- Bar Value Labels -->
                                <text 
                                    v-for="(item, index) in recentActivityData"
                                    :key="`value-${index}`"
                                    :x="140 + index * 120"
                                    :y="250 - (item.value / maxValue * 220) - 8"
                                    text-anchor="middle"
                                    fill="var(--new-primary)"
                                    font-size="14"
                                    font-weight="bold"
                                >
                                    {{ item.value }}
                                </text>
                                
                                <!-- X-axis Labels -->
                                <text 
                                    v-for="(item, index) in recentActivityData"
                                    :key="`label-${index}`"
                                    :x="140 + index * 120"
                                    y="275"
                                    text-anchor="middle"
                                    fill="var(--new-primary)"
                                    font-size="12"
                                    font-weight="bold"
                                >
                                    {{ item.label.replace(' Today', '') }}
                                </text>
                            </svg>
                        </div>
                        
                        <figcaption>Activity for the last 24 hours (Rates: {{ typeof rate === 'number' ? rate.toFixed(1) : rate }} gigs/hr created, {{ typeof dropped === 'number' ? dropped.toFixed(1) : dropped }} drops/hr)</figcaption>
                    </figure>
                </div>

                <!-- Stats Sections -->
                <div class="stats-section">
                    <h3>User Statistics</h3>
                    <div class="stat-container">
                        <div class="stat-widget users">
                            <h4 class="stat-number">{{ daters }}</h4> 
                            <span class="stat-label">Total Daters</span>
                        </div>
                        <div class="stat-widget users">
                            <h4 class="stat-number">{{ cupids }}</h4>
                            <span class="stat-label">Total Cupids</span>
                        </div>
                        <div class="stat-widget active">
                            <h4 class="stat-number">{{ active_cupids }}</h4> 
                            <span class="stat-label">Active Cupids</span>
                        </div>
                        <div class="stat-widget active">
                            <h4 class="stat-number">{{ active_daters }}</h4>
                            <span class="stat-label">Active Daters</span>
                        </div>
                    </div>
                </div>

                <div class="stats-section">
                    <h3>Gig Statistics</h3>
                    <div class="stat-container">
                        <div class="stat-widget gigs">
                            <h4 class="stat-number">{{ gigs }}</h4>
                            <span class="stat-label">Total Gigs</span>
                        </div>
                        <div class="stat-widget gigs">
                            <h4 class="stat-number">{{ typeof rate === 'number' ? rate.toFixed(1) : rate }}</h4>
                            <span class="stat-label">Gigs per Hour</span>
                        </div>
                        <div class="stat-widget completed">
                            <h4 class="stat-number">{{ typeof completed === 'number' ? (completed * 100).toFixed(1) + '%' : completed }}</h4>
                            <span class="stat-label">Completion Rate</span>
                        </div>
                        <div class="stat-widget dropped">
                            <h4 class="stat-number">{{ typeof dropped === 'number' ? dropped.toFixed(1) : dropped }}</h4>
                            <span class="stat-label">Drops per Hour</span>
                        </div>
                    </div>
                </div>
            </div>

            <button @click="toPDF" class="pdf-button">
                <span class="material-symbols-outlined">picture_as_pdf</span>
                Export to PDF
            </button>
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
    margin-top: 60px;
    padding-bottom: 120px;
}

/* Mobile: Add bottom padding for bottom navbar */
@media (max-width: 768px) {
    main {
        padding-bottom: 160px;
    }
}

/* Desktop: Add top margin for navbar below banner */
@media (min-width: 769px) {
    main {
        margin-top: 140px;
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

@media (max-width: 768px) {
    .header-bar {
        top: 60px;
    }
}

@media (min-width: 769px) {
    .header-bar {
        top: 140px;
        border-top: 2px solid var(--new-primary);
    }
}

.page-title {
    color: var(--new-primary);
    margin: 0;
    font-size: 2.2em;
    font-weight: bold;
}

.container {
    flex: 1;
    padding: 20px;
    margin-top: 80px;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
}

/* Chart Section */
.chart-section {
    margin-bottom: 40px;
    margin-top: 20px; /* Add top margin since widgets removed */
}

.graph-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: var(--new-secondary);
    border: 2px solid var(--new-primary);
    border-radius: 12px;
    padding: 20px;
    margin: 20px 0;
}

.graph {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
}

figcaption {
    color: var(--new-primary);
    margin-top: 12px;
    font-style: italic;
}

/* Graph placeholder */
.graph-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px;
    color: var(--new-primary);
    opacity: 0.7;
    min-height: 200px;
}

.graph-placeholder .material-symbols-outlined {
    font-size: 48px;
    margin-bottom: 12px;
    color: var(--new-light-blue);
}

.graph-placeholder p {
    margin: 0 0 8px 0;
    font-style: italic;
    font-size: 1.1em;
}

.placeholder-subtitle {
    font-size: 0.9em;
    opacity: 0.6;
}

/* Stats Sections */
.stats-section {
    margin-bottom: 30px;
}

.stats-section h3 {
    text-align: center;
    color: var(--new-primary);
    margin-bottom: 15px;
    font-size: 1.3em;
}

.stat-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 12px;
    align-items: center;
}

.stat-widget {
    border: 2px solid;
    border-radius: 8px;
    padding: 12px 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    transition: all 0.3s ease;
    min-width: 120px;
    max-width: 160px;
    flex: 0 1 auto;
}

.stat-widget:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.stat-widget.users {
    background-color: var(--new-secondary);
    border-color: var(--new-primary);
}

.stat-widget.active {
    background-color: var(--new-background);
    border-color: var(--new-light-blue);
}

.stat-widget.gigs {
    background-color: var(--new-background);
    border-color: var(--new-primary);
}

.stat-widget.completed {
    background-color: var(--new-primary);
    border-color: var(--new-primary);
    color: var(--new-background);
}

.stat-widget.dropped {
    background-color: var(--new-accent);
    border-color: var(--new-accent);
    color: white;
}

.stat-number {
    color: inherit;
    margin: 0 0 4px 0;
    font-size: 1.4em;
    font-weight: bold;
}

.stat-label {
    color: inherit;
    font-size: 0.85em;
    opacity: 0.9;
    line-height: 1.2;
}

/* PDF Button */
.pdf-button {
    display: flex;
    align-items: center;
    gap: 8px;
    background-color: var(--new-secondary);
    border: 2px solid var(--new-primary);
    border-radius: 8px;
    padding: 12px 24px;
    color: var(--new-primary);
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    margin: 20px auto;
}

.pdf-button:hover {
    background-color: var(--new-primary);
    color: var(--new-background);
    transform: translateY(-1px);
}

/* Bar Chart Styling */
.bar-chart-container {
    display: flex;
    justify-content: center;
    padding: 20px;
}

.bar-chart {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
}

.bar {
    transition: all 0.2s ease;
    cursor: pointer;
}

.bar:hover {
    opacity: 0.8;
    stroke-width: 3;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .stat-container {
        gap: 8px;
    }
    
    .stat-widget {
        min-width: 100px;
        max-width: 140px;
        padding: 10px 12px;
    }
    
    .stat-number {
        font-size: 1.2em;
    }
    
    .stat-label {
        font-size: 0.8em;
    }
    
    .container {
        margin-top: 60px;
        padding: 12px;
    }
}

@media (max-width: 480px) {
    .stat-container {
        gap: 6px;
    }
    
    .stat-widget {
        min-width: 80px;
        max-width: 120px;
        padding: 8px 10px;
    }
    
    .stat-number {
        font-size: 1.1em;
    }
    
    .stat-label {
        font-size: 0.75em;
    }
}
</style>





