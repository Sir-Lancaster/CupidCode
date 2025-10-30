<script setup>
import { makeRequest } from '../utils/make_request';
import {onMounted, ref, watch} from 'vue';
import router from '../router';

import NavSuite from '../components/NavSuite.vue';

const chatArr = ref([])
const message = ref('')
let noChats = false

const user_id  = parseInt(window.location.hash.split('/')[3])

const chatCount = 10;

async function getChats() {
    const results = await makeRequest(`/api/chat/${user_id}/${chatCount}`);
    console.log(results)
    // May need to split results chat to fit into array
    if (results === undefined) {
        chatArr.value = []
        noChats = true
    }
    else {
        chatArr.value = results.reverse()
    }
    console.log(chatArr.value)
}

async function send() {
    // Display on screen
    chatArr.value.push({
        owner: user_id,
        text: message.value,
        from_ai: false,
    })
    if (chatArr.length >= 1 && document.getElementById('header')) {
        document.getElementById("header").style.display = 'none';
        
    }

    // Send to server to save & get response from server
    const results = await makeRequest('/api/chat/', 'post', {
        user: {
            id: user_id
        },
        message: message.value
    });
    chatArr.value.push({
        owner: user_id,
        text: results.message,
        from_ai: true,
    })
}

onMounted(getChats)

</script>

<template>  
    <NavSuite title='Chat Room' profile='DaterProfile'>
        <router-link class="link" :to="{ name: 'DaterHome', params: {id: user_id} }"> Home </router-link>
        <router-link class="link" :to="{ name: 'DaterProfile', params: {id: user_id} }"> Profile </router-link>
        <router-link class="link" :to="{ name: 'Calendar', params: {id: user_id} }"> Calendar </router-link>
        <router-link class="link" :to="{ name: 'AiListen', params: {id: user_id} }"> AI Listen </router-link>
        <router-link class="link" :to="{ name: 'DaterGigs', params: {id: user_id}}"> Gigs </router-link>
        <router-link class="link" :to="{ name: 'CupidCash', params: {id: user_id} }"> Balance</router-link>
        <router-link class="link" :to="{ name: 'DaterFeedback', params: {id: user_id}}"> Feedback </router-link>
    </NavSuite>

    <div class="chatbox">
        <div v-if="noChats">
            <h3 id="header">Start your chat with Cupid AI here!</h3>
            <div id="chat-container"></div>
        </div>
        <div v-else>
            <div v-for="(chat, index) of chatArr" id="chat-container">
                <div :key="index" :class="chat.from_ai ? 'chat response' : 'chat sent'">{{ chat.text }}</div>
            </div>
        </div>
    </div>
    <div class="textbox">
        <label for="message" class="message">
            <h4>Enter Message Here</h4>
            <input id="message" placeholder="Type your message to the AI!" v-model="message">
        </label>
        <button class="button" @click="send">Send</button>
    </div>
</template>

<style scoped>
.chatbox {
    display: flex;
    flex-flow: column nowrap;
    overflow-y: scroll;
    height: 100%;
    margin-top: 42px;
    margin-bottom: 158px;
}

h3 {
    color: rgb(99, 99, 99);
    text-align: center;
}

.chat {
    padding: 8px;
    margin: 8px;
    border: none;
    border-radius: 4px;
}

.sent {
    display: flex;
    justify-content: flex-end;
    background-color: var(--primary-red);
    color: white;
    position: relative;
    margin-bottom: 10px;
    margin-left: calc(100% - 240px);
    padding: 10px;
}

.response {
    display: flex;
    justify-content: flex-start;
    background-color: var(--secondary-blue);
    color: white;
    position: relative;
    margin-bottom: 10px;
    margin-right: calc(100% - 240px);
    padding: 10px;
}

.textbox {
    display: flex;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    justify-content: center;
    align-content: center;
    flex-direction: column;
    background-color: var(--secondary-red);
    padding: 24px;
}


.message {
    text-align: center;
    color: white;
    display: flex;
    flex-direction: column;
}

.message h4 {
    margin: 4px;
    margin-top: 0px;
}

.message input {
    border: none;
    border-radius: 4px;
    padding: 8px;
    margin: 4px;
}

.button {
    border: none;
    border-radius: 4px;
    background-color: white;
    padding: 8px;
    margin: 4px 100px;
}

</style>
