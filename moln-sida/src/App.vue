<template>
  <div id="app">
    <div>
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>
    <router-view/>
  </div>
</template>

<style>
#app {
  height: 667px;
  width: 375px;
  background-image: url("https://wallpaperaccess.com/full/896979.jpg");
  background-size: cover;
}
</style>
