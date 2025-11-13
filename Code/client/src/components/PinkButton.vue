<script setup>
</script>
<template>
    <button :id="id" @click="$emit('click-forward')"><slot /></button>
</template>
<style scoped>
    button {
        margin-left: 3px;
        margin-right: 3px;
    background-color: var(--primary-red);
        border-radius: 10px;
    color: var(--on-button-text);
        border: none;
        border-radius: 4px;
        box-shadow: 5px 5px 2px rgba(0, 0, 0, 0.2);
        text-decoration: solid;
        padding: 16px;
        margin: auto;
        display: flex;
        justify-self: center;
        align-self: center;
        user-select: none;
    }

    button:hover {
        filter: brightness(0.9);
    }

    button:active {
        filter: brightness(0.7);
        transform: translate(3px,3px);
        box-shadow: 3px 3px 1px rgba(0, 0, 0, 0.4);
    }
</style>
