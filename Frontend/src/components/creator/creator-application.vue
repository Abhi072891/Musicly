<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <h2 class="mb-4">User Registration as Creator</h2>
          <router-link :to="'/home/' + userId" class="btn btn-secondary">Go back</router-link>
          <h5>User : {{ username }}</h5>
          <h5>{{ name }}</h5>
          <form @submit.prevent="submitForm">
            <div class="form-group">
              <label for="password">Password:</label>
              <p v-if="text" style="color: red;">{{ text }}</p>
              <input type="password" class="form-control" id="password" v-model="formData.password" required>
            </div>
            <div class="form-group">
              <p><h4>Your Actions must adhere to community guidelines</h4></p>
              <label for="responsibilities">Responsibilities as Creator:</label>
              <ul>
                <li>Create new Albums</li>
                <li>Edit an existing Album</li>
                <li>Assign a song to a particular album</li>
                <li>Upload new Songs</li>
                <li>Edit info or lyrics of existing song</li>
                <li>Remove an existing song/lyrics/album</li>
              </ul>
            </div>
            <div class="form-check mb-3">
              <input type="checkbox" class="form-check-input" id="agree" v-model="formData.agree" required>
              <label class="form-check-label" for="agree">I agree to the responsibilities as a creator</label>
            </div>
            <button type="submit" class="btn btn-primary">Register</button>
          </form>
        </div>
      </div>
    </div>
</template>

<script>
  export default {
    data() {
      return {
        userId: parseInt(localStorage.user_id), 
        username: localStorage.username, 
        name: localStorage.name, 
        formData: {
          password: '',
          agree: false
        },
        text: ''
      };
    },
    methods: {
      submitForm() {
        // Send POST request
        fetch(`http://127.0.0.1:5000/creator-application/${this.userId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.formData)
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          // Show alert and change localStorage status to 'wait'
          alert('Request sent successfully');
          localStorage.setItem('status', 'wait');
          // Redirect to home
          this.$router.push('/home');
        })
        .catch(error => {
          console.error('Error submitting form:', error);
          // Handle errors
        });
      }
    }
  };
</script>

<style scoped>
/* Your scoped styles */
</style>
  