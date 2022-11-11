<template>
  <div id="app">
    <div class="nav">
      <router-link to="/">Home</router-link>
      <router-link to="/about">About</router-link>
    </div>
    <router-view/>
  </div>
</template>

<style>
body {
  margin: 0px;
  padding: 0px;
}

#nav {
  align-content: center;
}

#app {
  height: 844px;
  width: 390px;
  display: flex;
  flex-direction: column;
  background-image: url("https://wallpaperaccess.com/full/896979.jpg");
  background-size: cover;
}
</style>
