<script setup>
import { makeRequest } from '../utils/make_request.js';
import { ref } from 'vue';
import router from '../router/index.js';

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
                <div class="button-container">
                    <button @click="$emit('click-forward')" class="action-button send-button">Sign In</button>
                </div>
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
    background-color: var(--new-background);
    align-items: center;
}

.form {
    display: flex;
    flex-flow: column wrap;
    background-color: var(--new-background);
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
    color: var(--new-primary);
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

.button-container {
    display: flex;
    justify-content: center;
}

/* Custom Action Buttons */
    .action-button {
        background-color: var(--new-background);
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
        width:50%;
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