<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
      <router-link class="navbar-brand" to="/home">Musicly</router-link>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/creator">Creator</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/home">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/songs">Songs</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/albums">Albums</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/artists">Artists</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/playlist">Playlists</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <router-view/>
</template>


<script>
export default {
  data() {
    return {
      
    };
  },
  mounted() {

  },
  methods: {
    
  },
};
</script>

<style scoped>

</style>

