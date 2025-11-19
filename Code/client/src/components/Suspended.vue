<script setup>

</script>

<template>
<div class="container">
    <div class="image">
        <img :src="'/get_img/'" alt="Cupid Code Logo" width="300" height="300">
    </div>
    <span>You are Suspended and cannot access your account.</span>
    <span>For more information, or to get unsuspended, please email us at </span>
    <a class="email">support@cupidcode.com</a>

    <router-link class="link suspended" to="/"> Go back to Home Page </router-link>
</div>
</template>

<style scoped>
.container {
    display: flex;
    flex-flow: column wrap;
    justify-content: center;
    align-content: center;
    color: black;
    margin: 10px;
    margin-top: 50px;
}

.container span {
    font-size: large;
}
.email {
    display: flex;
    align-self: center;
    border-bottom: 2px solid var(--primary-blue);
    color: var(--primary-blue);
    margin: 10px;
    font-size: xx-large;
    font-weight: bold;
}

.suspended {
    display: flex;
    align-self: center;
    justify-content: end;
    margin: 10px;
    margin-top: 40px;
    color: black;
}
</style>