<script setup>
import {ref} from 'vue'
import { makeRequest } from '../utils/make_request';

import PinkButton from '../components/PinkButton.vue';
import Popup from '../components/Popup.vue';
import NavSuite from '../components/NavSuite.vue';


let audio = null
let recorder = null

const popupActive = ref(false)
const budget = ref('')
const items_requested = ref('')
const pickup_location = ref('')

const user_id = parseInt(window.location.hash.split('/')[3])

function toggleEmergency() {
    popupActive.value = !popupActive.value;
}

async function sendEmergency() {
    const result = await makeRequest('/api/gig/create/', 'post', {
        "budget":budget._value,
        "items_requested":items_requested._value,
        "pickup_location":pickup_location._value
    })
    popupActive.value = false
}

async function listen() {
    // Request access to the user's microphone
    navigator.mediaDevices.getUserMedia({ audio: true })
    .then(function(stream) {
        // Create an instance of MediaRecorder to record audio
        recorder = new MediaRecorder(stream)
        let chunks = []
        // Start recording when the recorder is ready
        recorder.onstart = () => {console.log('Recording started')}
        // Collect recorded audio data in chunks
        recorder.ondataavailable = (event) => {chunks.push(event.data)}
        // Stop recording and process the recorded audio
        recorder.onstop = () => {
            // Combine all recorded chunks into a single Blob
            const audioBlob = new Blob(chunks, { type: 'audio/wav' });
            // Convert Blob to base64-encoded string
            const reader = new FileReader();
            reader.readAsDataURL(audioBlob);
            reader.onloadend = function() {
                const base64Data = reader.result.split(',')[1];
                // Send base64-encoded audio data to the backend for processing
                sendToBackend(base64Data);
            };
        };
        // Start recording
        recorder.start()
    })
    .catch(function(err) {
        console.error('Error accessing microphone:', err);
    })
}

// Function to send base64-encoded audio data to the backend
async function sendToBackend(base64Data) {
    // Example: Use fetch to send data to backend
    const res = await makeRequest('/api/stt/', 'post', {
        user_id, 
        audio: base64Data
    });
    console.log(res)
    // Put result on the screen
}

async function stopListen() {
    recorder.stop();
    recorder = null;
}
</script>

<template>
    <NavSuite title='Let the AI Listen in!' profile='DaterProfile'>
        <router-link class="link" :to="{ name: 'DaterHome', params: {id: user_id} }"> Home </router-link>
        <router-link class="link" :to="{ name: 'DaterProfile', params: {id: user_id} }"> Profile </router-link>
        <router-link class="link" :to="{ name: 'Calendar', params: {id: user_id} }"> Calendar </router-link>
        <router-link class="link" :to="{ name: 'AiChat', params: {id: user_id} }"> AI Chat </router-link>
        <router-link class="link" :to="{ name: 'DaterGigs', params: {id: user_id}}"> Gigs </router-link>
        <router-link class="link" :to="{ name: 'CupidCash', params: {id: user_id} }"> Balance</router-link>
        <router-link class="link" :to="{ name: 'DaterFeedback', params: {id: user_id}}"> Feedback </router-link>
    </NavSuite>

    <div class="container">
        <div class="buttons">
            <button class="listen button" @click="listen">
                <span class="material-symbols-outlined">mic</span>
            </button>
            <button class="listen button" @click="stopListen">
                <span class="material-symbols-outlined">mic_off</span>
            </button>
            <button class="emergency button" @click="toggleEmergency">
                <span class="material-symbols-outlined">priority_high</span>
            </button>
        </div>
        <Popup :data-active="popupActive">
            <h1>Create Gig</h1>
            <label class="update-content" for="budget">
                Budget
                <input type="text" id="budget" v-model="budget"/>
            </label>
            <label class="update-content" for="items_requested">
                Items Requested
                <input type="text" id="items_requested" v-model="items_requested"/>
            </label>
            <label class="update-content" for="pickup_location">
                Pickup Location
                <input type="text" id="pickup_location" v-model="pickup_location"/>
            </label>
            <div class="space-evenly">
                <PinkButton @click-forward="sendEmergency">Send</PinkButton>
                <PinkButton @click-forward="toggleEmergency">Cancel</PinkButton>
            </div>
        </Popup>
        <div class="text" id="chatbox">
        </div>
    </div>
</template>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-top: 40px;
}

.buttons {
    display: flex;
    justify-content: center;
    align-content: center;
}

.button {
    display: flex;
    justify-content: center;
    border: none;
    border-radius: 50%;
    height: 50%;
    padding: 30px;
    margin: 2px 4px;
        color: var(--on-button-text);
    box-shadow: 5px 5px 2px rgba(0, 0, 0, 0.2);
}

.button:hover {
    filter: brightness(0.6);
}

.listen {
    background-color: var(--secondary-blue);
}

.emergency {
    background-color: var(--secondary-red);
}

.text {
    display: flex;
    border-top: 4px solid var(--primary-red);
    margin: 10px;
    padding: 10px;
    justify-content: center;
    align-content: center;
    text-align: center;
}

.message {
    display: flex;
}

.space-evenly {
    display: flex;
    flex-direction: row;
    align-content: space-evenly;
}

.space-evenly > * {
    margin: 16px;
}

.popup h1 {
    margin: auto;
    margin-top: 12px;
    margin-bottom: 4px;
    width: fit-content;
}

.popup div {
    margin: auto;
}

.active {
    transform: scale(1);
    transition: transform 0.2s cubic-bezier(0,1.4,1,1);
}

    .update-content {
    text-align: center;
    margin-bottom: 4px;
    color: var(--new-primary);
    display: flex;
    flex-direction: column;
    align-items: center;
}

.update-content input{
    border: none;
    border-radius: 4px;
    padding: 8px;
}
</style>
