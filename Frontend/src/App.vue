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
          <li class="nav-item" v-show="!isAdmin">
            <router-link class="nav-link" to="/playlist">Playlists</router-link>
          </li>
          <li class="nav-item" v-show="!isAdmin">
            <router-link class="nav-link" to="/creator">Creator</router-link>
          </li>
          <li class="nav-item">
            <button class="nav-link btn btn-danger" @click="logout">Logout</button>
          </li>
          <li class="nav-item" v-show="!isAdmin">
            <router-link class="nav-link" to="/adminlogin">Admin Login</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <header class="hero bg-primary text-white text-center py-5" v-show="!logged_in">
        <div class="container">
            <h1 class="display-4">Discover the World of Music</h1>
            <p class="lead">Explore, listen, and create your own playlists.</p>
            <router-link to="/login" class="btn btn-light btn-lg" title="create your playslist">Get Started</router-link>
        </div>
  </header>
  <router-view/>
</template>


<script>
export default {
  data() {
    return {
      // localStorage: localStorage,
      isAdmin: false,
      logged_in: false
    };
  },
  mounted() {
    // this.checkLogin()
    this.isAdmin = localStorage.user_role === 'admin';
  },
  methods: {
    checkLogin() {
      if (!localStorage.token) {
        // Redirect to login page if token is not present
        this.$router.push('/login');
        return;
      }

      // Fetch request to check if token is valid
      fetch('http://127.0.0.1:5000/jwt/testing', {
        headers: {
          method: 'GET',
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.token}`
        }
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Authentication failed');
        }
      })
      .catch(error => {
        // Display alert and redirect to login page
        alert('Please log in.');
        this.$router.push('/login');
      });
    },
    logout() {
      if (confirm("Are you sure you want to log out")) {
        localStorage.clear();
        this.$router.push('/login');
      }
    }
  },
  watch: {
    '$route'() {
      this.isAdmin = localStorage.user_role === 'admin';
      this.logged_in = localStorage.logged_in === 'yes';
    }
  },
};
</script>

<style scoped>

</style>

