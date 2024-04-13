<template>
    <div>
      <h2>Edit Album</h2>
      <div class="form-group">
        <label for="albumName">Album Name:</label>
        <input type="text" id="albumName" v-model="editedAlbum.album_name" class="form-control">
      </div>
        <div class="form-group">
            <label for="artistNames">Artists:</label>
            <input type="text" id="artistNames" v-model="artistNames" class="form-control">
        </div>
      <div class="form-group">
        <label>Songs:</label>
        <div v-for="song in songs" :key="song.song_id">
          <input type="checkbox" :id="'song' + song.song_id" :value="song.song_id" v-model="selectedSongs" :checked="isSelected(song.song_id)">
          <label :for="'song' + song.song_id">{{ song.song_name }}</label>
        </div>
      </div>
      <button @click="updateAlbum" class="btn btn-primary">Update Album</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        editedAlbum: {}, 
        songs: [], 
        selectedSongs: [], 
        artistNames: ''
      };
    },
    mounted() {
      this.checkUser();
      this.fetchAlbum();
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
        
        if(localStorage.user_role==='user'){
            alert("not a creator")
            this.$router.push('/home')
        }
      },
      fetchAlbum() {
        fetch(`http://127.0.0.1:5000/albums/${parseInt(this.$route.params.albumId)}`,{
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.token}`
            }
          })
          .then(response => response.json())
          .then(data => {
            this.editedAlbum = data;
            this.selectedSongs = this.editedAlbum.songs.map(song => song.id);
            this.artistNames = this.editedAlbum.artists.map(artist => artist.name).join(', ');
          })
          .catch(error => console.error('Error fetching album:', error));
      },
      fetchSongs() {
        fetch(`http://127.0.0.1:5000/songsbyuser/${parseInt(localStorage.user_id)}`,{
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.token}`
            }
          })
          .then(response => response.json())
          .then(data => {
            this.songs = data;
          })
          .catch(error => {
            console.error('Error fetching songs:', error);
          });
      },
      isSelected(songId) {
        // Check if the song is already selected
        return this.selectedSongs.includes(songId);
      },
      updateAlbum() {
        this.editedAlbum.song_ids = this.selectedSongs;
        const artists = this.artistNames.split(',').map(artist => artist.trim());
        this.editedAlbum.artist_names = artists;
        fetch(`http://127.0.0.1:5000/albums/${parseInt(this.editedAlbum.album_id)}/${parseInt(localStorage.user_id)}`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.token}`
          },
          body: JSON.stringify(this.editedAlbum)
        })
        .then(response => {
          if (response.ok) {
            alert("Album has been edited successfully");
            this.$router.push({ name: 'creatordashboard' });
          } else {
            console.error('Error updating album');
          }
        })
        .catch(error => console.error('Error updating album:', error));
      }
    }
  };
</script>
  
<style scoped>

</style>
  