<script setup>
    import router from '../router/index'
    import { makeRequest } from '../utils/make_request'
    import {ref, onMounted} from 'vue'

    import CupidBanner from './components/CupidBanner.vue';
    import CupidNavBar from './components/CupidNavBar.vue';

    //User info
    const user_id  = parseInt(window.location.hash.split('/')[3]) //Gets the id from the router
    const email = ref('')
    const phone = ref('')
    const fname = ref('')
    const lname = ref('')
    const username = ref('')
    const paypal_email = ref('')

    //Cupid info
    const accepting_gigs = ref(false)
    const balance = ref(0)
    const range = ref(20)
    const gigs_completed = ref(0)
    const gigs_failed = ref(0)

    async function update() {
        // Validate data
        const checkData = [email, phone]

        let check = 0;
        for (let i = 0; i < checkData.length; i++) {
            if (checkData[i] !== '') check++;
            else {
                const error = document.querySelector(`input[name=${checkData[i]}]`);
                error.class = error.class + 'error';
            }
        }
        const results = await makeRequest(`/api/cupid/profile/`, 'post', {
            first_name: fname.value,
            last_name: lname.value,
            phone_number: phone.value,
            gig_range: range.value,
            paypal_email: paypal_email.value
        })
        router.push({name: 'CupidDetails', params: {id: user_id}});
    }

    async function getData() {
        const cupid = await makeRequest(`api/user/${user_id}`)
        email.value = cupid.user.email
        phone.value = cupid.user.phone_number
        fname.value = cupid.user.first_name
        lname.value = cupid.user.last_name
        username.value = cupid.user.username
        paypal_email.value = cupid.paypal_email

        accepting_gigs.value = cupid.accepting_gigs
        balance.value = cupid.cupid_cash_balance
        range.value = cupid.gig_range
        gigs_completed.value = cupid.gigs_completed
        gigs_failed.value = cupid.gigs_failed
    }

    onMounted(getData)

</script>

<template>
    <CupidBanner />
    <CupidNavBar currentPage="CupidDetails" />

    <main> 
        <div class="card">
            <h1>{{ fname }}'s Profile</h1>
            <hr></hr>
            <p id="succesful">{{ gigs_completed }} gigs successful of {{ gigs_failed + gigs_completed}}</p>
        </div>
        <h1>Update Details</h1>
        <hr>
        <form class="container" @submit.prevent="update">
            <label class="update-content" for="fname">
                First Name
                <input type="text" id="fname" v-model="fname"/>
            </label>
            <label class="update-content" for="lname">
                Last Name
                <input type="text" id="lname" v-model="lname"/>
            </label>
            <label class="update-content" for="phone">
                Phone Number
                <input type="number" id="phone" :placeholder="phone" v-model="phone"/>
            </label>
            <label class="update-content" for="range">
                Range
                <input type="text" id="range" v-model="range"/>
            </label>
            <button @click="$emit('click-forward')" class="action-button send-button margin-sixteen">Update Profile</button>
            <label class="form-field">
                PayPal Email (for receiving payments)
                <input type="email" v-model="paypal_email" required>
            </label>
            <PinkButton>Save</PinkButton>
        </form>
    </main>
</template>

<style scoped>

main {
    --new-primary: #09A129;     /* Green for text */
    --new-secondary: #1F487E;   /* Dark blue for buttons */
    --new-background: #000000;  /* Black for backgrounds */
    --new-accent: #FB3640;      /* Red */
    --new-light-blue: #00CCFF;  /* Light blue */
        
    padding: 20px;
    background-color: var(--new-background);
    color: var(--new-primary);
    min-height: 100vh;
        
    /* Spacing for Banner and NavBar */
    margin-top: 60px; /* Space for banner (60px) + gap */
}

/* Mobile: Add bottom margin for bottom navbar */
    @media (max-width: 768px) {
        main {
            margin-bottom: 90px; /* Space for bottom navbar */
        }
    }

    /* Desktop: Add top margin for navbar below banner */
    @media (min-width: 769px) {
        main {
            margin-top: 140px; /* Space for banner + navbar + gaps */
        }
    }

hr {
    border: 1px solid #F0F0F0;
    border-radius: 30%;
    margin: 6px;
}

.update-content {
    display: flex;
    flex-direction: column;
    padding: 8px;
    margin: 10px;
    font-weight: bold;
}

input {
    border: 3px rgba(128, 128, 128, 0.5) solid;
    border-radius: 4px;
    width: 100%;
    padding: 8px;
    margin-top: 5px;
    background-color: var(--new-background);
    color: white;
    box-sizing: border-box;
}

.card {
    border: 4px solid var(--new-background);
    border-radius: 16px;
    margin: 16px;
    padding: 8px;
    background-color: var(--new-background);
    color: var(--new-primary);
    font-size: 1.3em;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.card > hr {
    border-color: var(--new-accent);
}
.card > p {
    margin-top: 2px;
    margin-bottom: 2px;
    margin-left: auto;
    margin-right: auto;
}

/* Custom Action Buttons */
    .action-button {
        background-color: var(--new-secondary);
        border: 2px solid var(--new-primary);
        border-radius: 8px;
        padding: 12px 20px;
        color: var(--new-primary);
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 44px;
        min-width: 100px;
    }

    .action-button:hover {
        background-color: var(--new-primary);
        color: var(--new-background);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(9, 161, 41, 0.3);
    }

    .action-button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(9, 161, 41, 0.2);
    }

    .send-button {
        background-color: var(--new-secondary);
        border-color: var(--new-primary);
    }
</style>
