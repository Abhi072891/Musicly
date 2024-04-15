<template>
    <div class="container">
      <h1>Sign In</h1>
      <p >
        <router-link to="/register" class=" btn btn-secondary">Register</router-link>
      </p>
      <form @submit.prevent="submitForm">
        <p>
          <label>{{ form.username.label }}</label><br>
          <input v-model="formData.username" type="text"><br>
          <span v-for="error in formErrors.username" class="error">{{ error }}</span>
        </p>
        <p>
          <label>{{ form.password.label }}</label><br>
          <input v-model="formData.password_hash" type="password" id="myInput">
          <input type="checkbox" @click="myFunction()">Show Password <br>
          <span v-for="error in formErrors.password" class="error">{{ error }}</span>
        </p>
        <p><button type="submit" class="submit-button">Submit</button></p>
      </form>
    </div>
</template>
  
<script>

  export default {
    data() {
      return {
        form: {
          username: { label: 'Username' },
          password: { label: 'Password' }
        },
        formData: {
          username: '',
          password_hash: ''
        },
        formErrors: {
          username: [],
          password: []
        },
        text: ''
      };
    },
    methods: {
      submitForm() {
        fetch('http://127.0.0.1:5000/login', {
          method: 'POST',
          body: JSON.stringify(this.formData),
          headers: {
            'Content-Type': 'application/json'
          }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
          // console.log(data)
          if(data.user_role=='admin'){
            this.$router.push('/adminlogin')
            return
          }
          localStorage.setItem('token', data.access_token)
          localStorage.setItem('user_id',data.user_id)
          localStorage.setItem('user_role',data.user_role)
          localStorage.setItem('user_status',data.status)
          localStorage.setItem('name',data.name)
          localStorage.setItem('logged_in','yes')
          this.$router.push({name : 'home'})
        })
        .catch(error => {
          console.error('Error submitting form:', error);
        });
      },

      myFunction() {
        var x = document.getElementById("myInput");
        if (x.type === "password") {
          x.type = "text";
        } else {
          x.type = "password";
  }
}
    }
  };
</script>
  
<style scoped>
  /* Custom styles for the login page */
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
  
  p {
    color: #666;
    margin: 0 0 20px;
  }
  
  .error {
    color: red;
  }
  
  form {
    text-align: left;
  }
  
  input[type="text"],
  input[type="password"] {
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
  
  .register-link {
    color: #007BFF;
    text-decoration: none;
  }
  
  .register-link:hover {
    text-decoration: underline;
  }
</style>
  