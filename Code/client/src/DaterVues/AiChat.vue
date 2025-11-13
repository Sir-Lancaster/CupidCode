<script setup>
import { makeRequest } from '../utils/make_request';
import {onMounted, ref, watch} from 'vue';
import router from '../router';
import AIGigProposal from './components/AIGig.vue'
import { getCurrentLocation } from '../utils/location_utils'

import Banner from '../components/Banner.vue';
import NavBar from '../components/NavBar.vue';

const chatArr = ref([])
const message = ref('')
let noChats = false
let openAICheckTimeout = null
const checkedTranscripts = new Set() // To avoid duplicate checks

// Speech recognition variables
const isRecording = ref(false)
let recognition = null
let recordingTimeout = null

let keywordDetectedInSession = false
let processingKeywordCheck = false

const showAIGig = ref(false)
const proposedGig = ref(null)
const userLocation = ref(null)

// Use router params instead of hash extraction
const user_id = router.currentRoute.value.params.id
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
    // Stop recording if active before sending
    if (isRecording.value) {
        stopRecording()
    }
    
    // Don't send if message is empty
    if (!message.value.trim()) {
        return
    }
    
    // Reset noChats when sending a new message
    noChats = false
    
    // Display on screen
    chatArr.value.push({
        owner: user_id,
        text: message.value,
        from_ai: false,
    })
    if (chatArr.value.length >= 1 && document.getElementById('header')) {
        document.getElementById("header").style.display = 'none';
        
    }

    // Send to server to save & get response from server
    const results = await makeRequest('/api/chat/', 'post', {
        message: message.value
    });
    chatArr.value.push({
        owner: user_id,
        text: results.message,
        from_ai: true,
    })
    message.value = ''
}

function closeAIGig() {
    showAIGig.value = false
    proposedGig.value = null
}

function onGigCreated(gigData) {
    // Add success message to chat
    chatArr.value.push({
        owner: user_id,
        text: `Great! I've created your gig for ${proposedGig.value?.keyword}. A Cupid will pick it up soon! 🎉`,
        from_ai: true,
    })
    
    closeAIGig()
}

// Clear chat display function
function clearChatDisplay() {
    if (confirm('Clear chat display? This will hide all messages but won\'t delete your chat history.')) {
        chatArr.value = []
        noChats = true
        // Show the welcome header again
        if (document.getElementById('header')) {
            document.getElementById("header").style.display = 'block';
        }
    }
}

// Speech recognition functions
function toggleRecording() {
    if (isRecording.value) {
        stopRecording()
    } else {
        startRecording()
    }
}

function startRecording() {
    // Check for browser support
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert('Speech recognition not supported in this browser')
        return
    }

    keywordDetectedInSession = false
    processingKeywordCheck = false
    checkedTranscripts.clear()

    // Create recognition instance
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    recognition = new SpeechRecognition()
    
    // Configure recognition
    recognition.continuous = true  // allows for longer recordings 
    recognition.interimResults = true  // Changed to true to capture ongoing speech
    recognition.language = 'en-US'
    
    // Handle results
    recognition.onresult = (event) => {
        let finalTranscript = ''
        let interimTranscript = ''
        
        // Combine all final and interim results
        for (let i = 0; i < event.results.length; i++) {
            if (event.results[i].isFinal) {
                finalTranscript += event.results[i][0].transcript + ' '
            } else {
                // Real-time interim speech
                interimTranscript += event.results[i][0].transcript + ' '
            }
        }
        
        // Get the complete current transcript
        const completeTranscript = (finalTranscript + interimTranscript).trim()
        
        // Send to OpenAI for word detection 
        if (completeTranscript && !keywordDetectedInSession && !processingKeywordCheck) {
            checkForWordWithOpenAI(completeTranscript)
        }
        
        // Update message display
        if (completeTranscript) {
            message.value = completeTranscript
        }
    }

    async function checkForWordWithOpenAI(transcript) {
        if (keywordDetectedInSession || processingKeywordCheck) {
            return
        }
        // Debounce to avoid too many API calls
        if (openAICheckTimeout) {
            clearTimeout(openAICheckTimeout)
        }
        // Don't check the same transcript twice
        if (checkedTranscripts.has(transcript)) {
            return
        }
        
        openAICheckTimeout = setTimeout(async () => {
            try {
                processingKeywordCheck = true
                checkedTranscripts.add(transcript)
                
                console.log('🔍 Sending to OpenAI for product detection:', transcript)
                
                const response = await makeRequest('/api/check-speech-for-word/', 'post', {
                    transcript: transcript
                })

                if (response.word_detected) {
                    console.log('✅ OpenAI detected a sellable product:', response.detected_word)
                    
                    keywordDetectedInSession = true
                    const keyword = response.detected_word
                    
                    if (!userLocation.value) {
                        try {
                            userLocation.value = await getCurrentLocation()
                        } catch (error) {
                            console.warn('Could not get location:', error)
                        }
                    }
                    try {
                        console.log('🚀 Creating AI gig for product:', keyword)
                        const gigResponse = await makeRequest('/api/ai-gig/create/', 'post', {
                            keyword: keyword,
                            user_location: userLocation.value
                        })
                        
                        if (gigResponse.success) {
                            proposedGig.value = gigResponse.gig_data
                            showAIGig.value = true
                            console.log(`🎉 AI Gig created successfully for: ${keyword}`)
                        } else {
                            console.log(`❌ Could not create gig for ${keyword}:`, gigResponse.error)
                        }
                    } catch (error) {
                        console.error('💥 Error creating AI gig:', error)
                    }
                    console.log('🚫 Product detection disabled for remainder of this recording session')
                } else {
                    console.log('❌ No sellable products detected in:', transcript)
                    if (response.error) {
                        console.error('🔥 API Error:', response.error)
                    }
                    if (response.fallback_used) {
                        console.log('🔧 Fallback detection was used')
                    }
                }
            } catch (error) {
                console.error('💥 Error checking with OpenAI:', error)
            } finally {
                processingKeywordCheck = false
            }
        }, 100) // Wait 100ms after speech stops changing
    }
    
    // Handle errors
    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error)
        stopRecording()
    }
    
    // Handle end - restart if still recording (to prevent auto-stop)
    recognition.onend = () => {
        if (isRecording.value) {
            // Restart recognition if we're still supposed to be recording
            try {
                recognition.start()
            } catch (error) {
                console.error('Failed to restart recording:', error)
                stopRecording()
            }
        }
    }
    
    // Start recognition
    try {
        recognition.start()
        isRecording.value = true
        
        // Set 30-second timeout
        recordingTimeout = setTimeout(() => {
            stopRecording()
        }, 30000)
    } catch (error) {
        console.error('Failed to start recording:', error)
    }
}

function stopRecording() {
    if (recognition) {
        recognition.stop()
        recognition = null
    }
    if (recordingTimeout) {
        clearTimeout(recordingTimeout)
        recordingTimeout = null
    }
    if (openAICheckTimeout) {
        clearTimeout(openAICheckTimeout)
        openAICheckTimeout = null
    }
    processingKeywordCheck = false

    isRecording.value = false
}

onMounted(getChats)
</script>

<template>
    <Banner />
    <NavBar currentPage="AiChat" />

    <main>
        <!-- Fixed Header Bar -->
        <div class="header-bar">
            <h1 class="page-title">AI Chat</h1>
            <button @click="clearChatDisplay" class="clear-button" :disabled="chatArr.length === 0">
                <span class="material-symbols-outlined">cleaning_services</span>
                <span class="clear-text">Clear</span>
            </button>
        </div>
        
        <div class="chat-container">
            <!-- No chats state -->
            <div v-if="noChats" class="empty-state">
                <span class="material-symbols-outlined chat-icon">smart_toy</span>
                <h3 id="header">Start your chat with Cupid AI here!</h3>
                <p>Ask me anything about dating, relationships, or get personalized advice!</p>
            </div>
            
            <!-- Chat messages -->
            <div v-else class="messages-container">
                <div v-for="(chat, index) of chatArr" :key="index" class="message-wrapper">
                    <div :class="['message', chat.from_ai ? 'ai-message' : 'user-message']">
                        <div class="message-content">
                            <span v-if="chat.from_ai" class="material-symbols-outlined message-icon">smart_toy</span>
                            <span v-else class="material-symbols-outlined message-icon">person</span>
                            <p>{{ chat.text }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Message input -->
        <div class="input-container">
            <div class="input-wrapper">
                <button @click="toggleRecording" :class="['mic-button', { 'recording': isRecording }]">
                    <span class="material-symbols-outlined">{{ isRecording ? 'fiber_manual_record' : 'mic' }}</span>
                </button>
                <textarea 
                    v-model="message" 
                    @keyup.enter.exact="send"
                    @keydown.enter.shift.prevent
                    placeholder="Type your message to Cupid AI..."
                    class="message-input"
                    rows="1"
                ></textarea>
                <button @click="send" :disabled="!message.trim()" class="send-button">
                    <span class="material-symbols-outlined">send</span>
                </button>
            </div>
        </div>
            <!-- AI Gig Proposal Modal -->
        <AIGigProposal
            v-if="showAIGig && proposedGig"
            :gig-data="proposedGig"
            :user-id="user_id"
            @close="closeAIGig"
            @gig-created="onGigCreated"
         />
    </main>
</template>

<style scoped>
    /* New color scheme variables */
    main {
        --new-primary: #09A129;     /* Green for text */
        --new-secondary: #1F487E;   /* Dark blue for buttons */
        --new-background: #000000;  /* Black for backgrounds */
        --new-accent: #FB3640;      /* Red */
        --new-light-blue: #00CCFF;  /* Light blue */
        
        background-color: var(--new-background);
        color: var(--new-primary);
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        
        /* Spacing for Banner and NavBar */
        margin-top: 60px; /* Space for banner */
        padding-bottom: 120px; /* Changed from margin-bottom to padding-bottom */
    }

    /* Mobile: Add bottom padding for bottom navbar + input */
    @media (max-width: 768px) {
        main {
            padding-bottom: 180px; /* Increased space for navbar + input */
        }
    }

    /* Desktop: Add top margin for navbar below banner */
    @media (min-width: 769px) {
        main {
            margin-top: 140px; /* Space for banner + navbar + gaps */
            padding-bottom: 140px; /* Increased space for input container */
        }
    }

    /* Fixed Header Bar */
    .header-bar {
        position: fixed; /* Changed from sticky to fixed */
        top: 0;
        left: 0;
        right: 0;
        background-color: var(--new-background);
        border-bottom: 2px solid var(--new-primary);
        padding: 16px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 999; /* Lowered from 1002 to be below banner popup */
        margin-bottom: 0;
    }

    /* Mobile: Account for mobile navbar position */
    @media (max-width: 768px) {
        .header-bar {
            top: 60px; /* Below banner, navbar is at bottom */
        }
        
        .chat-container {
            margin-top: 120px; /* Space for banner + header bar */
            padding: 12px;
        }
    }

    /* Desktop: Position below banner and navbar with separator */
    @media (min-width: 769px) {
        .header-bar {
            top: 140px; /* Below banner (60px) + navbar (60px) + gaps (20px) */
            border-top: 2px solid var(--new-primary); /* Add green separator line */
        }
        
        .chat-container {
            margin-top: 200px; /* Space for banner + navbar + header bar */
            padding: 20px;
        }
    }

    .page-title {
        color: var(--new-primary);
        margin: 0;
        font-size: 2.2em;
        font-weight: bold;
    }

    .clear-button {
        display: flex;
        align-items: center;
        gap: 8px;
        background-color: var(--new-accent);
        border: 2px solid var(--new-accent);
        color: #FFFFFF;
        border-radius: 8px;
        padding: 10px 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 14px;
        font-weight: 500;
    }

    .clear-button:hover:not(:disabled) {
        background-color: #FFFFFF;
        color: var(--new-accent);
        transform: translateY(-1px);
    }

    .clear-button:disabled {
        background-color: var(--new-secondary);
        border-color: var(--new-secondary);
        color: var(--new-primary);
        opacity: 0.5;
        cursor: not-allowed;
        transform: none;
    }

    .clear-button .material-symbols-outlined {
        font-size: 18px;
    }

    /* Mobile: Hide text, show only icon */
    @media (max-width: 600px) {
        .clear-text {
            display: none;
        }
        
        .clear-button {
            padding: 10px 12px;
            min-width: 44px;
        }
        
        .page-title {
            font-size: 1.8em;
        }
    }

    .chat-container {
        flex: 1;
        padding: 20px;
        overflow-y: auto;
        padding-bottom: 40px; /* Extra padding at bottom */
    }

    /* Empty state styling */
    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 40px 20px;
        margin-top: 50px;
    }

    .chat-icon {
        font-size: 64px;
        color: var(--new-light-blue);
        margin-bottom: 20px;
    }

    .empty-state h3 {
        color: var(--new-primary);
        margin: 16px 0;
        font-size: 1.4em;
    }

    .empty-state p {
        color: var(--new-primary);
        opacity: 0.8;
        max-width: 400px;
        line-height: 1.5;
    }

    /* Messages container */
    .messages-container {
        display: flex;
        flex-direction: column;
        gap: 16px;
        padding-bottom: 60px; /* Increased bottom padding */
        min-height: 100%; /* Ensure it fills available space */
    }

    .message-wrapper {
        width: 100%;
    }

    .message {
        max-width: 45%; /* this changes the width of the message bubbles */
        word-wrap: break-word;
    }

    .user-message {
        margin-left: auto;
        margin-right: 0;
    }

    .ai-message {
        margin-left: 0;
        margin-right: auto;
    }

    .message-content {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 16px;
        border-radius: 12px;
        border: 2px solid;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    .user-message .message-content {
        background-color: var(--new-secondary);
        border-color: var(--new-primary);
        flex-direction: row-reverse;
    }

    .ai-message .message-content {
        background-color: var(--new-background);
        border-color: var(--new-light-blue);
    }

    .message-icon {
        font-size: 24px;
        flex-shrink: 0;
        margin-top: 2px;
    }

    .user-message .message-icon {
        color: var(--new-primary);
    }

    .ai-message .message-icon {
        color: var(--new-light-blue);
    }

    .message-content p {
        margin: 0;
        color: var(--new-primary);
        line-height: 1.5;
        flex: 1;
    }

    /* Input container */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: var(--new-background);
        border-top: 2px solid var(--new-primary);
        padding: 16px;
        z-index: 1000; /* Increased z-index to be above navbar */
    }

    /* Mobile: Account for bottom navbar */
    @media (max-width: 768px) {
        .input-container {
            bottom: 80px; /* Increased to be clearly above navbar */
            z-index: 1001; /* Higher than navbar z-index */
        }
    }

    .input-wrapper {
        display: flex;
        gap: 12px;
        max-width: 800px;
        margin: 0 auto;
        align-items: flex-end; /* Changed from center to flex-end for better alignment */
    }

    /* Microphone Button */
    .mic-button {
        background-color: var(--new-secondary);
        border: 2px solid var(--new-primary);
        color: var(--new-primary);
        border-radius: 8px;
        padding: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 48px;
        height: 48px;
    }

    .mic-button:hover {
        background-color: var(--new-primary);
        color: var(--new-background);
        transform: translateY(-1px);
    }

    .mic-button.recording {
        background-color: var(--new-accent);
        border-color: var(--new-accent);
        color: #FFFFFF;
        animation: pulse 1.5s infinite;
    }

    .mic-button.recording:hover {
        background-color: var(--new-accent);
        color: #FFFFFF;
        transform: none;
    }

    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }

    .mic-button .material-symbols-outlined {
        font-size: 20px;
    }

    .message-input {
        flex: 1;
        padding: 12px 16px;
        border: 2px solid var(--new-primary);
        border-radius: 8px;
        background-color: var(--new-background);
        color: var(--new-primary);
        font-size: 16px;
        outline: none;
        transition: all 0.3s ease;
        resize: none;
        min-height: 48px;
        max-height: 120px;
        overflow-y: auto;
        font-family: inherit;
        line-height: 1.4;
    }

    .message-input:focus {
        border-color: var(--new-light-blue);
        box-shadow: 0 0 0 2px rgba(0, 204, 255, 0.2);
    }

    .message-input::placeholder {
        color: var(--new-primary);
        opacity: 0.6;
    }

    /* Auto-resize textarea */
    .message-input {
        field-sizing: content;
    }

    /* Fallback for browsers that don't support field-sizing */
    @supports not (field-sizing: content) {
        .message-input {
            height: auto;
        }
    }

    .send-button {
        background-color: var(--new-secondary);
        border: 2px solid var(--new-primary);
        color: var(--new-primary);
        border-radius: 8px;
        padding: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 48px;
        height: 48px;
    }

    .send-button:hover:not(:disabled) {
        background-color: var(--new-primary);
        color: var(--new-background);
        transform: translateY(-1px);
    }

    .send-button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
        transform: none;
    }

    .send-button .material-symbols-outlined {
        font-size: 20px;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .message {
            max-width: 85%; /* Slightly smaller on mobile */
        }
        
        .message-content {
            padding: 12px;
        }
        
        .input-wrapper {
            gap: 8px;
        }
    }
</style>
