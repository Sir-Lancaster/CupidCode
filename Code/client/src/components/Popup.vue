<template>
    <div class="popup" data-active="false">
        <slot />
    </div>
</template>
<style scoped>
    .popup {
        position: fixed;
        width: clamp(220px, 50%, 400px);
        height: fit-content;
        margin: auto;
        padding: 20px;
        left: 0;
        right: 0;
        top: 30%;

        transform: scale(0);
        transition: transform 0.2s cubic-bezier(0,1,1,1);

        display: flex;
        flex-direction: column;
        align-content: flex-end;
        background-color: var(--new-secondary);
        border: 3px solid var(--new-light-blue);
        color: var(--new-primary);
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 204, 255, 0.3);
        z-index: 1000;
    }

    .popup[data-active="true"] {
        transform: scale(1);
        transition: transform 0.2s cubic-bezier(0,1.4,1,1);
    }
</style>
