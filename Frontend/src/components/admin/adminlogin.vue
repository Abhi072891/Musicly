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
        const credentials = {
          username: this.username,
          password: this.password
        };
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
          return response.json()
        })
        .then(data => {
          console.log(data)
          localStorage.setItem('token', data.access_token)
          localStorage.setItem('user_id',data.user_id)
          localStorage.setItem('user_role',data.user_role)
          localStorage.setItem('user_status',data.status)
          localStorage.setItem('name',data.name)
          localStorage.setItem('logged_in','yes')
          this.$router.push('/admindashboard')
        })
        .catch(error => {
          console.error('Login failed:', error);
          alert('Login failed. Please check your credentials and try again.');
          window.location.reload();
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
  