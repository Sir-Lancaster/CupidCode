<script setup>
import { makeRequest } from '../utils/make_request.js';
import { ref } from 'vue';
import router from '../router/index.js';

// For both accounts
const email = ref('')
const password = ref('')
const accType = ref('dater')
const fname = ref('')
const lname = ref('')
const username = ref('')
const showError = ref(false)
const errorMsg = ref('')
const payemail = ref('')
let image = null 

// Field-specific error tracking
const fieldErrors = ref({
    fname: '',
    lname: '',
    username: '',
    email: '',
    password: '',
    payemail: ''
})

function validateField(fieldName, value) {
    fieldErrors.value[fieldName] = ''
    
    switch (fieldName) {
        case 'fname':
            if (!value.trim()) {
                fieldErrors.value[fieldName] = 'First name is required'
            } else if (value.trim().length < 2) {
                fieldErrors.value[fieldName] = 'First name must be at least 2 characters'
            }
            break
        case 'lname':
            if (!value.trim()) {
                fieldErrors.value[fieldName] = 'Last name is required'
            } else if (value.trim().length < 2) {
                fieldErrors.value[fieldName] = 'Last name must be at least 2 characters'
            }
            break
        case 'username':
            if (!value.trim()) {
                fieldErrors.value[fieldName] = 'Username is required'
            } else if (value.trim().length < 3) {
                fieldErrors.value[fieldName] = 'Username must be at least 3 characters'
            }
            break
        case 'email':
            if (!value.trim()) {
                fieldErrors.value[fieldName] = 'Email is required'
            } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
                fieldErrors.value[fieldName] = 'Please enter a valid email address'
            }
            break
        case 'password':
            if (!value) {
                fieldErrors.value[fieldName] = 'Password is required'
            } else if (value.length < 6) {
                fieldErrors.value[fieldName] = 'Password must be at least 6 characters'
            }
            break
        case 'payemail':
            if (accType.value === 'cupid') {
                if (!value.trim()) {
                    fieldErrors.value[fieldName] = 'PayPal email is required for Cupid accounts'
                } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
                    fieldErrors.value[fieldName] = 'Please enter a valid PayPal email address'
                }
            }
            break
    }
}

function validateAllFields() {
    validateField('fname', fname.value)
    validateField('lname', lname.value)
    validateField('username', username.value)
    validateField('email', email.value)
    validateField('password', password.value)
    
    if (accType.value === 'cupid') {
        validateField('payemail', payemail.value)
    }
    
    // Check if any field has errors
    return Object.values(fieldErrors.value).every(error => error === '')
}

async function register() {
    try {
        showError.value = false
        errorMsg.value = ''
        
        if (!validateAllFields()) {
            return
        }

        if (accType.value === 'dater') {
            const results = await makeRequest('/api/user/create/', 'post', {
                username: username.value,
                first_name: fname.value,
                last_name: lname.value,
                email: email.value,
                password: password.value,
                role: accType.value
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
                paypal_email: payemail.value
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
                    <label class="radio_detail" for="dater">
                        Dater
                        <input type="radio" id="dater" name="accountType" value="dater" v-model="accType"/>
                    </label>
                    <label class="radio_detail" for="cupid">
                        Cupid 
                        <input type="radio" id="cupid" name="accountType" value="cupid" v-model="accType"/>
                    </label>
                </div>

                <div class="name-picture-section">
                    <div class="name-fields">
                        <label class="form_input" for="fname">
                            <span v-if="fieldErrors.fname" class="field-error">{{ fieldErrors.fname }}</span>
                            First Name *
                            <input 
                                type="text" 
                                id="fname" 
                                placeholder="First Name" 
                                v-model="fname"
                                @blur="validateField('fname', fname)"
                                :class="{ 'error-field': fieldErrors.fname }"
                            />
                        </label>
                        <label class="form_input" for="lname">
                            <span v-if="fieldErrors.lname" class="field-error">{{ fieldErrors.lname }}</span>
                            Last Name *
                            <input 
                                type="text" 
                                id="lname" 
                                placeholder="Last Name" 
                                v-model="lname"
                                @blur="validateField('lname', lname)"
                                :class="{ 'error-field': fieldErrors.lname }"
                            />
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
                    <span v-if="fieldErrors.username" class="field-error">{{ fieldErrors.username }}</span>
                    Username *
                    <input 
                        type="text" 
                        id="username" 
                        placeholder="username01" 
                        v-model="username"
                        @blur="validateField('username', username)"
                        :class="{ 'error-field': fieldErrors.username }"
                    />
                </label>
                <label class="form_input" for="email">
                    <span v-if="fieldErrors.email" class="field-error">{{ fieldErrors.email }}</span>
                    Email *
                    <input 
                        type="email" 
                        id="email" 
                        placeholder="example@email.com" 
                        v-model="email" 
                        required
                        @blur="validateField('email', email)"
                        :class="{ 'error-field': fieldErrors.email }"
                    />
                </label>
                <label class="form_input" for="password">
                    <span v-if="fieldErrors.password" class="field-error">{{ fieldErrors.password }}</span>
                    Password *
                    <input 
                        type="password" 
                        id="password" 
                        placeholder="Password" 
                        v-model="password" 
                        required
                        @blur="validateField('password', password)"
                        :class="{ 'error-field': fieldErrors.password }"
                    />
                </label>

                <div v-if="accType === 'cupid'" class="cupid_fields">
                    <h3>Cupid Information</h3>
                    <label class="form_input" for="payemail">
                        <span v-if="fieldErrors.payemail" class="field-error">{{ fieldErrors.payemail }}</span>
                        PayPal Email *
                        <input 
                            type="email" 
                            id="payemail" 
                            placeholder="example@email.com" 
                            v-model="payemail" 
                            required
                            @blur="validateField('payemail', payemail)"
                            :class="{ 'error-field': fieldErrors.payemail }"
                        />
                    </label>
                </div>

                <button @click="$emit('click-forward')" class="action-button send-button">Create Account</button>
            </form>
        </div>
        <div class="atag">
            Already have an account?
            <router-link to="/">Sign in here!</router-link>
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
    margin: 10px 0;
    padding: 10px;
    border-radius: 4px;
    font-weight: bold;
}

.field-error {
    display: block;
    color: var(--new-accent);
    background-color: rgba(251, 54, 64, 0.1);
    font-size: 14px;
    font-weight: bold;
    padding: 5px 8px;
    border-radius: 4px;
    margin-bottom: 5px;
    border-left: 3px solid var(--new-accent);
}

.error-field {
    border-color: var(--new-accent) !important;
    background-color: rgba(251, 54, 64, 0.05) !important;
}

.register_paper {
    display: flex;
    flex-flow: column wrap;
    background-color: var(--new-background);
    align-items: center;
    width: 100%;
}

.form {
    display: flex;
    flex-flow: column wrap;
    background-color: var(--new-background);
    border: 3px solid var(--new-primary);
    width: 100%;
    max-width: 600px; 
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 10px;
    box-sizing: border-box;
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

/* Mobile responsive adjustments */
@media (max-width: 768px) {
    main {
        padding: 10px;
    }
    
    .form {
        padding: 15px;
        margin: 0 5px 20px 5px;
    }
    
    .name-picture-section {
        flex-direction: column;
        gap: 10px;
    }
    
    .name-fields {
        width: 100%;
    }
    
    .profile-picture-section {
        width: 100%;
    }
    
    .radios {
        flex-direction: column;
        gap: 10px;
    }
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
    padding: 8px 0;
    font-weight: bold;
    width: 100%;
}

input, textarea {
    border: 3px rgba(128, 128, 128, 0.5) solid;
    border-radius: 4px;
    width: 100%;
    padding: 8px;
    margin: 5px 0;
    background-color: var(--new-background);
    color: var(--new-primary);
    box-sizing: border-box;
}

input[type="file"] {
    border: none;
    color: var(--new-primary);
    width: auto;
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

.cupid_fields {
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
    margin: 10px 0;
    box-sizing: border-box;
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