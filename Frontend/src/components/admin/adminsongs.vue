<template>
  <div v-if="songs.length > 0">
    <h2>Songs :</h2>
    <ul class="list-group">
      <li v-for="song in songs" :key="song.song_id" class="list-group-item">
        <div class="d-flex justify-content-between align-items-center">
          <span>{{ song.song_name }}</span>
          <div class="btn-group">
            <button @click="deleteSong(song.song_id)" class="btn btn-danger">Delete</button>
            <router-link :to="'/songinfo/' + song.song_id" class="btn btn-primary">Go to Song</router-link>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
    export default {
    data() {
      return {
        songs: [],
      };
    },
    mounted() {
      this.checkUser();
      this.fetchSongs();
    },
    methods: {
      checkUser(){
        if (!localStorage.token) {
          alert("Login again")
          this.$router.push('/login');
        }
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
          alert('Please log in again.');
          this.$router.push('/login');
        });

        if(localStorage.user_role!="admin"){
            alert('not a admin')
            window.location.reload()
        }
      },
      fetchSongs() {
        fetch(`http://127.0.0.1:5000/songs/0`,{
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.token}`
          }
        })
        .then(respose => respose.json())
        .then(data => {
            this.songs=data
        })
        .catch(error => console.log(error))
      },
      deleteSong(songId) {
        if (confirm("Are you sure you want to delete this song?")) {
            fetch(`http://127.0.0.1:5000/songs/${parseInt(songId)}`, {
              method: 'DELETE',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.token}`
              }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Song deleted successfully:', data);
                alert("Song deleted successfully");
                window.location.reload()
            })
            .catch(error => {
                console.error('Error deleting song:', error);
                alert("Error in deleting song")
                window.location.reload()
            });
        }
      },
    }
  };
</script>

<style scoped>

</style>