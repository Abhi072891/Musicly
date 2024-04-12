<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <h2 class="mb-4">Creators List</h2>
          <router-link to="/home" class="btn btn-secondary mb-3">Go back</router-link>
          <div v-for="creator in creators" :key="creator.user_id" class="card mb-3">
            <div class="card-body">
              <h5 class="card-title">{{ creator.username }}</h5>
              <p class="card-text">Status: {{ creator.status }}</p>
              <button v-if="creator.status === 'wlc'" @click="blacklistCreator(creator.user_id)" class="btn btn-danger">Blacklist</button>
              <button v-else-if="creator.status === 'blc'" @click="whitelistCreator(creator.user_id)" class="btn btn-success">Whitelist</button>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>
  
<script>
  export default {
    data() {
      return {
        creators: []
      };
    },
    mounted() {
      this.fetchCreators();
    },
    methods: {
      fetchCreators() {
        fetch('http://127.0.0.1:5000/allcreators')
          .then(response => response.json())
          .then(data => {
            this.creators = data;
          })
          .catch(error => {
            console.error('Error fetching creators:', error);
          });
      },
      whitelistCreator(userId) {
        fetch(`http://127.0.0.1:5000/creatorwhitelist/${userId}`)
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            console.log('Creator whitelisted successfully');
            this.fetchCreators(); // Refresh the list of creators
          })
          .catch(error => {
            console.error('Error whitelisting creator:', error);
          });
      },
      blacklistCreator(userId) {
        fetch(`http://127.0.0.1:5000/creatorblacklist/${userId}`)
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            console.log('Creator blacklisted successfully');
            this.fetchCreators(); // Refresh the list of creators
          })
          .catch(error => {
            console.error('Error blacklisting creator:', error);
          });
      }
    }
  };
</script>
  
<style>
/* Add your CSS styles here */
</style>
  