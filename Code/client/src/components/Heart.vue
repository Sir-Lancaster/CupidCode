<script setup>
    const props = defineProps(['active'])
</script>
<template>
    <!--https://www.svgrepo.com/svg/532473/heart-->
    <svg class = "heart" :data-active="active" viewBox="0 0 24 24">
        <path fill-rule="evenodd" clip-rule="evenodd" d="M12 6.00019C10.2006 3.90317 7.19377 3.2551 4.93923 5.17534C2.68468 7.09558 2.36727 10.3061 4.13778 12.5772C5.60984 14.4654 10.0648 18.4479 11.5249 19.7369C11.6882 19.8811 11.7699 19.9532 11.8652 19.9815C11.9483 20.0062 12.0393 20.0062 12.1225 19.9815C12.2178 19.9532 12.2994 19.8811 12.4628 19.7369C13.9229 18.4479 18.3778 14.4654 19.8499 12.5772C21.6204 10.3061 21.3417 7.07538 19.0484 5.17534C16.7551 3.2753 13.7994 3.90317 12 6.00019Z" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        </path>
    </svg>
</template>
<style scoped>
    .heart {
        /* New color scheme variables - same as other components */
        --new-primary: #09A129;     /* Green for text */
        --new-secondary: #1F487E;   /* Dark blue for buttons */
        --new-background: #000000;  /* Black for backgrounds */
        --new-accent: #FB3640;      /* Red */
        --new-light-blue: #00CCFF;  /* Light blue */
        
        background-color: transparent;
        margin: 4px;
        width: 50px;
        height: 50px;
        display: flex;
        justify-content: center;
        align-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        fill: var(--new-background);
    }

    .heart:hover {
        transform: scale(1.1);
        fill: var(--new-accent);
    }

    .heart[data-active=true] {
        fill: var(--new-accent);
        transform: scale(1.05);
    }
    
    .heart[data-active=true] > path {
        stroke: var(--new-primary);
        stroke-width: 2.5;
    }

    .heart > path {
        stroke: var(--new-primary);
        stroke-width: 2;
        transition: all 0.3s ease;
    }
</style>
