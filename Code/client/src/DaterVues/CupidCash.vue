<script setup>
    import {ref, onMounted} from 'vue';
    import router from '../router/index';
    import { makeRequest } from '../utils/make_request';

    import Banner from '../components/Banner.vue';
    import NavBar from '../components/NavBar.vue';


    const user_id  = parseInt(window.location.hash.split('/')[3])

    const balance = ref(0)
    const cards = ref([])
    const cardIndex = ref(0)
    const amount = ref(0)

    const chosenCard = ref(0)

    const name = ref('')
    const num = ref('')
    const mon = ref('')
    const year = ref('')
    const cvv = ref('')

    async function addFunds() {
        const res = await makeRequest('/api/dater/transfer/', 'post', {
            user: user_id,
            card_id: chosenCard.value,
            amount: amount
        })
    }

    async function saveCard() {
        // Save card to db
        const exp = `${mon.value}/${year.value}`

        const res = await makeRequest('/api/dater/save_card/', 'post', {
            user: {
                id: user_id
            },
            name_on_card: name.value,
            card_number: num.value,
            cvv: cvv.value,
            expiration: exp
        })
        const card_id = res.id
        const new_res = await makeRequest('/api/dater/transfer/', 'post', {
            user: user_id,
            card_id: card_id,
            amount: amount
        })

        router.push({name: 'CupidCash', params: {id: user_id}})
    }


    async function getMoney() {
        const results = await makeRequest(`/api/dater/balance/${user_id}`)
        balance.value = results.balance
        
        cards.value = await makeRequest(`/api/dater/get_cards/${user_id}`)
        console.log(cards)
    }

    onMounted(getMoney)   
</script>

<template>  
    <Banner />
    <NavBar currentPage="Home" />

    <main>

    <div class="container center">
        <h1>{{ 'Current balance: $' + balance }}</h1>
        <form class="container clamped" @submit.prevent="addFunds">
            <select v-model="cardIndex">
                <option disabled selected>Saved cards</option>
                <option v-for="(card, i) in cards" :value="i">***{{ card.card_number.slice(card.card_number.length-4) }}</option>
            </select>
            <div class="oneline">
                <input type="number" min="0" id="amount" v-model="amount"/>
                <button class="button">Deposit</button>
            </div>
        </form>
        <h1>Add Card</h1>
        <form class="input-container clamped" @submit.prevent="saveCard">
            <label class="details" for="card-name">  
                <input type="text" name="card-name" id="card-name" placeholder="Name on Card"
                :value="name" @change="e => name = e.target.value"
                >
            </label>
            <label class="details" for="card-num">  
                <input type="text" name="card-num" id="card-num" placeholder="0000 0000 0000 0000"
                :value="num" @change="e => num = e.target.value"
                >
            </label>
            <div class="date">
                <label class="details" for="month">  
                    <input type="text" size="5" name="month" id="month" placeholder="MM"
                    :value="mon" @change="e => mon = e.target.value"
                    >
                </label>
                <label class="details" for="year">  
                    <input type="text" size="5" name="year" id="year" placeholder="YY"
                    :value="year" @change="e => year = e.target.value"
                    >
                </label>
                <label class="details" for="security-code">  
                    <input type="text" size="5" name="security-code" id="security-code" placeholder="CVV"
                    :value="cvv" @change="e => cvv = e.target.value">
                </label>
            </div>
            <button class="button">Save Card</button>
        </form>
    </div>
    </main>
</template>

<style scoped>
    main {
        padding: 20px;
        background-color: var(--new-background);
        color: var(--new-primary);
        min-height: 100vh;

        /* Fixed spacing for Banner and NavBar */
        padding-top: 80px; /* Space for banner + navbar + gap */
        margin-top: 0;
    }

    /* Mobile: Add bottom margin for bottom navbar */
    @media (max-width: 768px) {
        main {
            padding-top: 60px; /* Space for banner + extra spacing on mobile */
            padding-bottom: 140px; /* Space for bottom navbar */
        }
    }

    /* Desktop: Add top margin for navbar below banner */
    @media (min-width: 769px) {
        main {
            padding-top: 160px; /* Space for banner + navbar + gaps */
        }
    }



.container h1 {
    margin-top: 50px;
    text-align: center;
}

.container {
    display: flex;
    justify-content: center;
    align-content: center;
    margin-left: 12px;
    margin-right: 12px;
    flex-direction: column;

    background-color: var(--new-background);
    border: 3px solid var(--new-primary);
    width: 100%;
    max-width: 600px;
    padding: 20px;
    border-radius: 10px;
    box-sizing: border-box;
}

.input-container input {
    border: none;
    box-sizing: border-box;
    outline: 0;
    padding: 12px;
    width: 100%;
}

.oneline {
    display: flex;
    flex-direction: row;
}

select,
.oneline > input{
    margin: auto;
    display: flex;
    border: 1px solid rgb(139, 139, 139);
    border-radius: 4px;
    padding: 12px;
    color: rgb(139, 139, 139);
    width: 100%;
}

select {
    color: black;
}

.center {
    display: flex;
    flex-direction: column;
    align-content: center;
}

.center > * {
    margin: auto;
}

.clamped {
    width: clamp(230px, 50%, 400px);
}

.details input{
    display: flex;
    margin: 4px;
    border: 1px solid rgb(139, 139, 139);
    gap: 8px;
    border-radius: 4px;
    padding: 16px;
    color: rgb(139, 139, 139);
}

.date {
    display: flex;
    flex-direction: row;
}

.button {
    display: flex;
    justify-content: center;
    align-content: center;
    border: none;
    border-radius: 8px;
    padding: 16px;
    margin: 10px;
    color: var(--on-button-text);
    background-color: var(--secondary-red);
}

input:focus {
    border-color: var(--secondary-red);
}

</style>
