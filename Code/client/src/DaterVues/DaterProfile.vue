<script setup>
    import {ref, onMounted} from 'vue';
    import router from '../router/index';
    import { makeRequest } from '../utils/make_request';

    import Banner from '../components/Banner.vue';
    import NavBar from '../components/NavBar.vue';

    const email = ref('')
    const phone = ref('')
    const addr = ref('')
    const fname = ref('')
    const lname = ref('')
    const username = ref('')
    const desc = ref('')
    const showError = ref(false)
    const errorMsg = ref('')
    let image = null 
    const str = ref('')
    const weak = ref('')
    const ntype = ref('')
    const interests = ref('')
    const goals = ref('')
    const past = ref('')
    const degree = ref('')

    // Allow user to change password
    const oldPassword = ref('')
    const newPassword = ref('')
    const newPassword2 = ref('')
    
    const user_id  = parseInt(window.location.hash.split('/')[3])

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

    async function getData() {
        try {
            const results = await makeRequest(`api/user/${user_id}`)
            degree.value = results.ai_degree
            addr.value = results.location
            desc.value = results.description
            str.value = results.dating_strengths
            weak.value = results.dating_weaknesses
            ntype.value = results.nerd_type
            interests.value = results.interests
            goals.value = results.relationship_goals
            past.value = results.past

            email.value = results.user['email']
            fname.value = results.user['first_name']
            lname.value = results.user['last_name']
            phone.value = results.user['phone_number']
            username.value = results.user['username']
        } catch (error) {
            showError.value = true
            errorMsg.value = 'Failed to load profile data'
        }
    }

    async function update() {
        try {
            const results = await makeRequest(`/api/dater/profile/`, 'post', {
                username: username.value,
                first_name: fname.value,
                last_name: lname.value,
                email: email.value,
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
                ai_degree: degree.value,
            })
            
            if (results.Reason) {
                showError.value = true
                errorMsg.value = results.Reason
                return
            }
            
            showError.value = false
            router.push({name: 'DaterProfile', params: {id: user_id}});
        } catch (error) {
            showError.value = true
            errorMsg.value = 'Failed to update profile'
        }
    }
    
    async function updatePassword() {
        if (newPassword.value !== newPassword2.value) {
            showError.value = true
            errorMsg.value = 'Passwords do not match'
            return
        }
        // TODO: Implement password update
        console.log("Password update not yet implemented")
    }

    onMounted(getData)

</script>

<template>
    <Banner />
    <NavBar currentPage="Home" />
    <main>
        <span v-if="showError" class="error">{{ errorMsg }}</span>

        <!-- Box 1: Personal Information -->
        <div class="form-box">
            <h2>Personal Information</h2>      
            <div class="form-grid">
                <label class="form_input" for="fname">
                    First Name
                    <input type="text" id="fname" v-model="fname"/>
                </label>
                <label class="form_input" for="lname">
                    Last Name
                    <input type="text" id="lname" v-model="lname"/>
                </label>
                <label class="form_input" for="phone">
                    Phone Number
                    <input type="tel" id="phone" v-model="phone"/>
                </label>
                <label class="form_input" for="address">
                    Address
                    <input type="text" id="address" v-model="addr"/>
                </label>
                <label class="form_input full-width" for="degree">
                    AI Assistance Level
                    <select id="degree" v-model="degree">
                        <option value="I don't want any help">I don't want any help</option>
                        <option value="I would like a little help">I would like a little help</option>
                        <option value="I need a good amount of help">I need a good amount of help</option>
                        <option value="I need all the help">I need all the help</option>
                    </select>
                </label>
            </div>
        </div>

        <!-- Box 2: User Information with Profile Picture -->
        <div class="form-box">
            <h2>User Information</h2>
            <div class="userinfo-container">
                <div class="userinfo-fields">
                    <label class="form_input" for="username">
                        Username
                        <input type="text" id="username" v-model="username"/>
                    </label>
                    <label class="form_input" for="email">
                        Email
                        <input type="email" id="email" v-model="email"/>
                    </label>
                </div>
                <div class="profile-picture-section">
                    <img name="pfp" src="" height="150" width="150" alt="Image preview" class="pfp-preview">
                    <label class="form_input side_by_side" for="image">
                        Profile Picture
                        <input type="file" id="image" name="image" @change="previewFile"/>
                    </label>
                </div>
            </div>
        </div>

        <!-- Box 3: Details About You -->
        <form class="form-box" @submit.prevent="update">
            <h2>Details About You</h2>
            <div class="form-grid">
                <label class="form_input full-width" for="desc">
                    Physical Description
                    <textarea id="desc" v-model="desc" rows="3"></textarea>
                </label>
                <label class="form_input full-width" for="nerd_type">
                    Nerd Type
                    <input type="text" id="nerd_type" v-model="ntype" placeholder="e.g., Gamer, Book Nerd"/>
                </label>
                <label class="form_input full-width" for="interests">
                    Interests
                    <textarea id="interests" v-model="interests" rows="3"></textarea>
                </label>
                <label class="form_input full-width" for="goals">
                    Relationship Goals
                    <textarea id="goals" v-model="goals" rows="3"></textarea>
                </label>
                <label class="form_input full-width" for="past">
                    Past Dating History
                    <textarea id="past" v-model="past" rows="3"></textarea>
                </label>
                <label class="form_input full-width" for="strengths">
                    Dating Strengths
                    <textarea id="strengths" v-model="str" rows="3"></textarea>
                </label>
                <label class="form_input full-width" for="weaknesses">
                    Dating Weaknesses
                    <textarea id="weaknesses" v-model="weak" rows="3"></textarea>
                </label>
            </div>
            <button @click="$emit('click-forward')" class="action-button send-button margin-sixteen">Update Profile</button>
        </form>

        <!-- Box 4: Update Password -->
        <form class="form-box" @submit.prevent="updatePassword">
            <h2>Update Password</h2>
            <div class="form-grid">
                <label class="form_input full-width" for="old-password">
                    Old Password
                    <input type="password" id="old-password" v-model="oldPassword"/>
                </label>
                <label class="form_input full-width" for="new-password">
                    New Password
                    <input type="password" id="new-password" v-model="newPassword">
                </label>
                <label class="form_input full-width" for="new-password-2">
                    Repeat New Password
                    <input type="password" id="new-password-2" v-model="newPassword2"/>
                </label>
            </div>
            <button @click="$emit('click-forward')" class="action-button send-button margin-sixteen">Update Password</button>
        </form>
    </main>
</template>

<style scoped>
main {
    --new-primary: #09A129;
    --new-secondary: #1F487E;
    --new-background: #000000;
    --new-accent: #FB3640;
    --new-light-blue: #00CCFF;
    
    padding: 40px;
    background-color: var(--new-background);
    color: var(--new-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    gap: 20px;
    align-items: center;
    margin-top: 60px;
    box-sizing: border-box;
}

@media (max-width: 768px) {
    main {
        margin-bottom: 95px;
    }
}

@media (min-width: 769px) {
    main {
        margin-top: 140px;
    }
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
    width: 100%;
    max-width: 600px;
}

.form-box {
    display: flex;
    flex-direction: column;
    background-color: black;
    border: 3px solid var(--new-primary);
    width: 100%;
    max-width: 600px;
    padding: 20px;
    border-radius: 10px;
    box-sizing: border-box;
}

h2 {
    text-align: center;
    color: var(--new-primary);
    margin: 0 0 20px 0;
}

.form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
}

@media (max-width: 600px) {
    .form-grid {
        grid-template-columns: 1fr;
    }
}

.full-width {
    grid-column: 1 / -1;
}

.form_input {
    display: flex;
    flex-direction: column;
    font-weight: bold;
    padding: 8px;
}

.side_by_side {
    flex-direction: column;
    align-items: center;
    width: 100%;
    max-width: none;
}

input, textarea, select {
    border: 3px rgba(128, 128, 128, 0.5) solid;
    border-radius: 4px;
    width: 100%;
    padding: 8px;
    margin-top: 5px;
    background-color: var(--new-background);
    color: white;
    box-sizing: border-box;
}

input[type="file"] {
    border: none;
    color: var(--new-primary);
}

textarea {
    resize: vertical;
    font-family: inherit;
}

select {
    cursor: pointer;
}

.userinfo-container {
    display: flex;
    gap: 20px;
    margin-bottom: 10px;
}

@media (max-width: 600px) {
    .userinfo-container {
        flex-direction: column;
    }
}

.userinfo-fields {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.profile-picture-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    flex: 1;
}

.pfp-preview {
    border: 3px solid var(--new-primary);
    border-radius: 8px;
    object-fit: cover;
    background-color: rgba(9, 161, 41, 0.1);
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