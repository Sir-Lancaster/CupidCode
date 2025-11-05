<script setup>
    import router from '../router/index'
    import { makeRequest } from '../utils/make_request'
    import {ref, onMounted} from 'vue'

    import NavSuite from '../components/NavSuite.vue';
    import CupidCoin from './components/CupidCoin.vue'
    import PinkButton from '../components/PinkButton.vue'

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

    async function toggleAccept() {
        accepting_gigs.value = !accepting_gigs.value
        await makeRequest(`/api/cupid/accepting/`, `post`, {
            'choice': accepting_gigs.value
        })
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
    <NavSuite title='Profile' profile='CupidDetails'>
        <router-link class="link" :to="{name: 'CupidHome', params: {id: user_id}}"> Home </router-link>
        <router-link class="link" :to="{name: 'GigDetails', params: {id: user_id}}"> Gigs Available </router-link>
        <router-link class="link" :to="{name: 'GigComplete', params: {id: user_id}}"> Gigs Completed </router-link>
        <router-link class="link" :to="{name: 'CupidFeedback', params: {id: user_id}}"> Feedback </router-link>
    </NavSuite>

    <main> 
        <CupidCoin :active="accepting_gigs" @click="toggleAccept"/>
        <div class="card">
            <p id="balance">${{ balance }}</p>
            <hr></hr>
            <p id="succesful">{{ gigs_completed }} gigs succesful of {{ gigs_failed + gigs_completed}}</p>
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
    position: absolute;
    top: 42px;
    left: 0px;
    right: 0px;
    padding: 8px;
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
    width: auto;
    padding: 8px;
    margin: 10px;
}

.card {
    border: 4px solid var(--secondary-blue);
    border-radius: 16px;
    margin: 16px;
    padding: 8px;
    background-color: var(--primary-blue);
    color: white;
    font-size: 1.3em;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.card > hr {
    border-color: var(--secondary-red);
}
.card > p {
    margin-top: 2px;
    margin-bottom: 2px;
    margin-left: auto;
    margin-right: auto;
}
</style>
