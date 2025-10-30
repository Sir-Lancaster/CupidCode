<script setup>
import { makeRequest } from '../utils/make_request.js';
import { ref } from 'vue';
import router from '../router/index.js';
import PinkButton from '../components/PinkButton.vue'

const email = ref('')
const password = ref('')
const showError = ref(false)
const errorMsg = ref('')

async function login() {
    try {
        const results = await makeRequest('/api/user/sign_in/', 'post', {
            email: email.value,
            password: password.value,
        })
        
        // Check if this is an error response with a Reason
        if (results.Reason) {
            showError.value = true
            errorMsg.value = results.Reason
            return;
        }
        
        // Successful response - hide error
        showError.value = false
        
        if (results.is_suspended) {
            router.push('/suspended')
        }
        else if (results.user && results.user['role']) {
            const role = results.user['role'].toLowerCase()
            if (role === 'dater') {
                router.push({name: 'DaterHome', params: {id: results.user['id']}})
            } else if (role === 'cupid') {
                router.push({name: 'CupidHome', params: {id: results.user['id']}})
            } else if (role === 'manager') {
                router.push({name: 'ManagerHome', params: {id: results.user['id']}})
            } else {
                router.push('/login')
            }
        }
    } catch (error) {
        showError.value = true
        errorMsg.value = 'Email or Password is wrong!'
    }
}
</script>

<template>
    <main>
        <div class="login_paper">
            <div class="image">
                <img :src="'/get_img/'" alt="Cupid Code Logo">
            </div>
            <form class="form" @submit.prevent="login">
                <span v-if="showError" class="error">{{ errorMsg }}</span>
                <label class="form_input" for="email">
                    Email
                    <input type="email" placeholder="example@email.com" id="email" name="email" v-model="email">
                </label>
                <label class="form_input" for="password">
                    Password
                    <input type="password" placeholder="Password" id="password" name="password" v-model="password">
                </label>
                <PinkButton id="sign_in">Sign In</PinkButton>
            </form>
        </div>
        <div class="atag">
            Don't have an account?
            <router-link to="/register">Sign up here!</router-link>
        </div>
    </main>
</template>

<style scoped>
main {
    --new-primary: #09A129;
    --new-secondary: #1F487E;
    --new-background: #000000;
    --new-accent: #FB3640;
    --new-light-blue: #00CCFF;
    
    padding: 20px;
    background-color: var(--new-background);
    color: var(--new-primary);
    min-height: 100vh;
}

.error {
    display: block;
    text-align: center;
    color: var(--new-accent);
    background-color: rgba(251, 54, 64, 0.1);
    margin: 10px;
    padding: 10px;
    border-radius: 4px;
    font-weight: bold;
}

.login_paper {
    display: flex;
    flex-flow: column wrap;
    background-color: black;
    align-items: center;
}

.form {
    display: flex;
    flex-flow: column wrap;
    background-color: black;
    border: 3px solid var(--new-primary);
    width: 100%;
    max-width: 600px; 
    padding-bottom: 20px;
    margin-bottom: 20px;
    border-radius: 10px;
}

.form_input {
    display: flex;
    flex-direction: column;
    padding: 8px;
}

input {
    border: 3px rgba(128, 128, 128, 0.5) solid;
    border-radius: 4px;
    width: auto;
    padding: 8px;
    margin: 10px;
    background-color: var(--new-background);
    color: white;
}

.atag {
    display: flex;
    margin: 10px;
    justify-content: center;
    align-items: center;
}

a {
    margin: 10px;
    color: var(--new-light-blue);
}

a:hover {
    color: gray;
}

.image {
    width: 100%;
    max-width: 600px;
    margin-bottom: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.image img {
    width: 100%;
    height: auto;
    display: block;
}
</style>