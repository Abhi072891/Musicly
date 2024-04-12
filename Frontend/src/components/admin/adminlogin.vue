<template>
    <div class="container">
      <h2>Admin Login</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="username">Username:</label>
          <input type="text" class="form-control" id="username" v-model="username" required>
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" class="form-control" id="password" v-model="password" required>
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
      </form>
    </div>
</template>

<script>
  export default {
    data() {
      return {
        username: '',
        password: ''
      };
    },
    methods: {
      login() {
        // Perform login authentication here, e.g., sending a POST request to the server
        const credentials = {
          username: this.username,
          password: this.password
        };
  
        // Example of sending a POST request using fetch
        fetch('http://127.0.0.1:5000/admin/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(credentials)
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Login failed');
          }
          // Redirect to admin dashboard upon successful login
          this.$router.push('/admindashboard');
        })
        .catch(error => {
          console.error('Login failed:', error);
          // Show an alert or error message to the user
          alert('Login failed. Please check your credentials and try again.');
        });
      }
    }
  };
</script>

<style scoped>
  .container {
    max-width: 400px;
    margin: auto;
    padding-top: 50px;
  }
  .form-group {
    margin-bottom: 20px;
  }
</style>
  