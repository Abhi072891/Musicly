<template>
    <div class="container">
      <h1>Create Album</h1>
      <form @submit.prevent="createAlbum">
        <div class="form-group">
          <label for="albumName">Album Name:</label>
          <input type="text" id="albumName" v-model="albumName" required class="form-control">
        </div>
        <div class="form-group">
          <label>Songs:</label>
          <!-- <select v-model="selectedSongs" multiple class="form-control">
            <option v-for="song in songs" :key="song.song_id" :value="song.song_id">{{ song.song_name }}</option>
          </select> -->
        <!-- <select v-model="selectedSongs" multiple class="form-control">
            <option v-for="song in songs" :key="song.song_id" :value="song.song_id">{{ song.song_name }}</option>
        </select> -->
        <div v-for="song in songs" :key="song.song_id" class="form-check">
            <input type="checkbox" :id="'song_' + song.song_id" :value="song.song_id" v-model="selectedSongs" class="form-check-input">
            <label :for="'song_' + song.song_id" class="form-check-label">{{ song.song_name }}</label>
        </div>


        </div>
        <button type="submit" class="btn btn-primary">Create Album</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        albumName: '',
        selectedSongs: [],
        songs: []
      };
    },
    mounted() {
      this.fetchSongs();
    },
    methods: {
      fetchSongs() {
        fetch(`http://127.0.0.1:5000/songsbyuser/${parseInt(localStorage.user_id)}`)
          .then(response => response.json())
          .then(data => {
            this.songs = data;
          })
          .catch(error => {
            console.error('Error fetching songs:', error);
          });
      },
      createAlbum() {
        const formData = {
          album_name: this.albumName,
          song_ids: this.selectedSongs
        };
        fetch(`http://127.0.0.1:5000/albums/${parseInt(localStorage.user_id)}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.token}`
          },
          body: JSON.stringify(formData)
        })
          .then(response => response.json())
          .then(data => {
            console.log('Album created:', data);
            this.$router.push({ name: 'creatordashboard' });
          })
          .catch(error => {
            console.error('Error creating album:', error);
          });
      }
    }
  };
  </script>
  
  <style>
  /* Add your component-specific styles here */
  </style>
  