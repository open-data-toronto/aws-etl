<template>
  <div class="navbar">
    <sui-menu fluid borderless>
      <sui-menu-item>
        <img src="../assets/logo.png" size="tiny" alt="logo">
      </sui-menu-item>
      <sui-menu-item header>
        <router-link to="/">Home</router-link>
      </sui-menu-item>
      <sui-menu-item header>
        <router-link to="/dashboard">Dashboard</router-link>
      </sui-menu-item>
    </sui-menu>
  </div>
</template>

<script>
export default {
  name: 'TheNavbar'
}
</script>
