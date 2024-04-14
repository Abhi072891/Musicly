<template>
  <div class="container">
    <h1>Register</h1>
    <router-link to="/login" class="btn btn-secondary">Login</router-link>
    <form @submit.prevent="submitForm">
      <p>
        <label for="name">Name:</label><br>
        <input type="text" id="name" v-model="formData.name" class="form-control">
        <span v-for="error in formErrors.name" class="error">{{ error }}</span>
      </p>
      <p>
        <label for="age">Age:</label><br>
        <input type="number" id="age" v-model="formData.age" class="form-control">
        <span v-for="error in formErrors.age" class="error">{{ error }}</span>
      </p>
      <p>
        <label for="gender">Gender:</label><br>
        <select id="gender" v-model="formData.gender" class="form-control">
          <option value="">Select gender</option>
          <option value="male">Male</option>
          <option value="female">Female</option>
          <option value="other">Other</option>
        </select>
        <span v-for="error in formErrors.gender" class="error">{{ error }}</span>
      </p>
      <p>
        <label for="username">Username:</label><br>
        <input type="text" id="username" v-model="formData.username" class="form-control" @blur="checkUsernameAvailability">
        <span v-if="!isValidUsername" class="error">Username is already taken</span>
      </p>
      <p>
        <label for="email">Email:</label><br>
        <input type="email" id="email" v-model="formData.email" class="form-control" required>
        <span v-if="!isValidEmail" class="error">Please enter a valid email address</span>
        <span v-if="!isUniqueEmail" class="error">Email is already registered</span>
      </p>
      <p>
        <label for="password">Password:</label><br>
        <input type="password" id="password" v-model="formData.password_hash" class="form-control" required>
        <span v-if="!isValidPassword" class="error">Password must be at least 15 characters long</span>
      </p>

      <p><button type="submit" class="submit-button btn btn-primary" :disabled="!isFormValid">Register</button></p>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      formData: {
        name: '',
        age: 18,
        gender: '',
        username: '',
        email:'',
        password_hash: ''
      },
      formErrors: {
        email: [],
        username: [],
        password: [],
        name: [],
        age: [],
        gender:[],
      },
      text: '',
      isValidUsername: true,
      isValidEmail: true,
      isUniqueEmail: true,
      isValidPassword: true,
    };
  },
  computed: {
    isFormValid() {
      return this.isValidEmail && this.isUniqueEmail && this.isValidUsername && this.isValidPassword;
    }
  },
  methods: {
    submitForm() {
      console.log('Form submitted:', this.formData);
      fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        body: JSON.stringify(this.formData),
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to register');
        }
        return response.json();
      })
      .then(data => {
        console.log(data)
        this.$router.push({name : 'login'})
      })
      .catch(error => {
        console.error('Error submitting form:', error);
      });
    },
    async checkUsernameAvailability() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/check-username/${this.formData.username}`);
        const data = await response.json();
        this.isValidUsername = data.available; 
      } catch (error) {
        console.error('Error checking username availability:', error);
      }
    },
    async validateEmail(email) {
      try {
          const response = await fetch(`http://127.0.0.1:5000/check-email/${email}`);
          const data = await response.json();
          this.isUniqueEmail = data.available;
      } catch (error) {
          console.error('Error checking email availability:', error);
      }
    },
  },
  watch: {
    'formData.username'(newValue) {
      if (newValue) {
        this.checkUsernameAvailability();
      }
    },
    'formData.email'(newValue) {
      if (newValue) {
        this.validateEmail(newValue);
      }
    }
  }
};

</script>

  
<style scoped>
  /* Custom styles for the registration page */
  .container {
    background-color: #fff;
    border-radius: 5px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
    padding: 20px;
    max-width: 400px;
    width: 90%;
  }
  h1 {
    color: #333;
    font-size: 2.5rem;
    margin: 0 0 20px;
  }
  .error {
    color: red;
  }
  form {
    text-align: left;
  }
  input[type="text"],
  input[type="number"],
  input[type="password"],
  select {
    width: 100%;
    padding: 10px;
    margin: 8px 0;
    border: 1px solid #ccc;
    border-radius: 3px;
    background-color: #f8f8f8;
  }
  .submit-button {
    background-color: #333;
    color: #fff;
    border: none;
    padding: 10px 15px;
    border-radius: 3px;
    cursor: pointer;
  }
  .submit-button:hover {
    background-color: #222;
  }
</style>
  