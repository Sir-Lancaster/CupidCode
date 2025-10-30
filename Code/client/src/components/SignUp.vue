<script setup>
import { makeRequest } from '../utils/make_request.js';
import { ref } from 'vue';
import router from '../router/index.js';
import PinkButton from '../components/PinkButton.vue'

// For both accounts
const email = ref('')
const password = ref('')
const accType = ref('')
const phone = ref('')
const addr = ref('')
const fname = ref('')
const lname = ref('')
const username = ref('')
const desc = ref('')
const showError = ref(false)
const errorMsg = ref('')
let image = null 

// Dater specific 
const str = ref('')
const weak = ref('')
const ntype = ref('')
const interests = ref('')
const goals = ref('')
const past = ref('')

async function register() {
    try {
        // Validate required fields
        if (!email.value || !password.value || !accType.value || !phone.value || !addr.value) {
            showError.value = true
            errorMsg.value = 'Please fill in all required fields'
            return
        }

        if (accType.value === 'dater') {
            const results = await makeRequest('/api/user/create/', 'post', {
                username: username.value,
                first_name: fname.value,
                last_name: lname.value,
                email: email.value,
                password: password.value,
                role: accType.value,
                phone_number: phone.value,
                location: addr.value,
                description: desc.value,
                //profile_picture: image,
                dating_strengths: str.value,
                dating_weaknesses: weak.value,
                nerd_type: ntype.value,
                interests: interests.value,
                relationship_goals: goals.value,
                past: past.value,
            })
            
            if (results.Reason) {
                showError.value = true
                errorMsg.value = results.Reason
                return
            }
            
            showError.value = false
            router.push({name: 'DaterHome', params: {id: results.user['id']}})
        }
        else if (accType.value === 'cupid') {
            const results = await makeRequest('/api/user/create/', 'post', {
                username: username.value,
                first_name: fname.value,
                last_name: lname.value,
                email: email.value,
                password: password.value,
                role: accType.value,
                phone_number: phone.value,
                location: addr.value,
                description: desc.value,
                //profile_picture: image
            })
            
            if (results.Reason) {
                showError.value = true
                errorMsg.value = results.Reason
                return
            }
            
            showError.value = false
            router.push({name: 'CupidHome', params: {id: results.user['id']}})
        }
        else {
            showError.value = true
            errorMsg.value = 'Please select an account type'
        }
    } catch (error) {
        showError.value = true
        errorMsg.value = 'Registration failed. Please try again.'
    }
}

function previewFile() {
    let preview = document.querySelector('img[name=pfp]');
    let file = document.querySelector('input[type=file]').files[0];
    let reader = new FileReader();
    
    image = file

    reader.onloadend = function () {
        preview.src = reader.result;
    }

    if (file) {
        reader.readAsDataURL(file);
    } else {
        preview.src = "";
    }
}
</script>

<template>
    <main>
        <div class="register_paper">
            <div class="image">
                <img :src="'/get_img/'" alt="Cupid Code Logo">
            </div>
            <h1>Create Your Account!</h1>
            <form class="form" @submit.prevent="register">
                <span v-if="showError" class="error">{{ errorMsg }}</span>
                
                <h3>Account Type</h3>
                <div class="radios">
                    <label class="radio_detail" for="cupid">
                        Cupid 
                        <input type="radio" id="cupid" name="accountType" value="cupid" v-model="accType"/>
                    </label>
                    <label class="radio_detail" for="dater">
                        Dater
                        <input type="radio" id="dater" name="accountType" value="dater" v-model="accType"/>
                    </label>
                </div>

                <div class="name-picture-section">
                    <div class="name-fields">
                        <label class="form_input" for="fname">
                            First Name *
                            <input type="text" id="fname" placeholder="First Name" v-model="fname"/>
                        </label>
                        <label class="form_input" for="lname">
                            Last Name *
                            <input type="text" id="lname" placeholder="Last Name" v-model="lname"/>
                        </label>
                    </div>
                    <div class="profile-picture-section">
                        <img name="pfp" src="" height="150" width="150" alt="Image preview" class="pfp-preview" style="margin-top: 10px;">

                        <label class="form_input side_by_side" for="image">
                            Profile Picture
                            <input type="file" id="image" name="image" @change="previewFile"/>
                        </label>
                    </div>
                </div>

                <label class="form_input" for="username">
                    Username *
                    <input type="text" id="username" placeholder="username01" v-model="username"/>
                </label>
                <label class="form_input" for="email">
                    Email *
                    <input type="email" id="email" placeholder="example@email.com" v-model="email" required/>
                </label>
                <label class="form_input" for="password">
                    Password *
                    <input type="password" id="password" placeholder="Password" v-model="password" required/>
                </label>
                <label class="form_input" for="phone">
                    Phone Number *
                    <input type="tel" id="phone" placeholder="8889991111" v-model="phone" required/>
                </label>
                <label class="form_input" for="address">
                    Address *
                    <input type="text" id="address" placeholder="1300 N 400 W Example Lane" v-model="addr" required/>
                </label>
                <label class="form_input" for="desc">
                    Physical Description
                    <textarea id="desc" v-model="desc" rows="4"></textarea>
                </label>

                <div v-if="accType === 'dater'" class="dater_fields">
                    <h3>Dater Information</h3>
                    <label class="form_input" for="nerd_type">
                        Nerd Type
                        <input type="text" id="nerd_type" v-model="ntype" placeholder="e.g., Gamer, Book Nerd, Tech Enthusiast"/>
                    </label>
                    <label class="form_input" for="goals">
                        Relationship Goals
                        <textarea id="goals" v-model="goals" rows="3"></textarea>
                    </label>
                    <label class="form_input" for="interests">
                        Interests
                        <textarea id="interests" v-model="interests" rows="3"></textarea>
                    </label>
                    <label class="form_input" for="past">
                        Past Dating History
                        <textarea id="past" v-model="past" rows="3"></textarea>
                    </label>
                    <label class="form_input" for="strengths">
                        Dating Strengths
                        <textarea id="strengths" v-model="str" rows="3"></textarea>
                    </label>
                    <label class="form_input" for="weaknesses">
                        Dating Weaknesses
                        <textarea id="weaknesses" v-model="weak" rows="3"></textarea>
                    </label>
                </div>

                <PinkButton>Create Account</PinkButton>
            </form>
        </div>
        <div class="atag">
            Already have an account?
            <router-link to="/login">Sign in here!</router-link>
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

.register_paper {
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
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 10px;
}

.side_by_side {
    flex-direction: column;
    align-items: center;
    width: 100%;
    max-width: none;
}

h1 {
    text-align: center;
    color: var(--new-primary);
    margin-bottom: 20px;
}

h3 {
    text-align: center;
    color: var(--new-primary);
    margin: 10px 0;
}

.radios {
    display: flex;
    flex-flow: row wrap;
    justify-content: center;
    align-items: center;
    gap: 20px;
    margin: 10px 0 20px 0;
}

.radio_detail {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--new-primary);
    font-weight: bold;
}

.radio_detail input[type="radio"] {
    margin: 0;
    cursor: pointer;
}

.name-picture-section {
    display: flex;
    gap: 20px;
    align-items: flex-start;
}

.name-fields {
    flex: 1;
}

.profile-picture-section {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.pfp-preview {
    border: 3px solid var(--new-primary);
    border-radius: 8px;
    object-fit: cover;
}

.form_input {
    display: flex;
    flex-direction: column;
    padding: 8px;
    font-weight: bold;
}

input, textarea {
    border: 3px rgba(128, 128, 128, 0.5) solid;
    border-radius: 4px;
    width: auto;
    padding: 8px;
    margin: 10px;
    background-color: var(--new-background);
    color: white;
}

input[type="file"] {
    border: none;
    color: var(--new-primary);
}

textarea {
    resize: vertical;
    font-family: inherit;
}

.dater_fields {
    border-top: 2px solid var(--new-primary);
    margin-top: 20px;
    padding-top: 10px;
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