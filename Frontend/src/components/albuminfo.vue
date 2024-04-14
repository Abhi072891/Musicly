<template>
  <div class="container">
    <h2 class="text-center mt-5 mb-4">{{ album.album_name }}</h2>

    <div class="mb-5">
      <h5>Artists of Album <span class="font-italic">{{ album.album_name }}</span>:</h5>
      <ol class="list-group">
        <li v-for="artist in album.artists" :key="artist.id" class="list-group-item">
          <router-link :to="'/artists/' + artist.id" class="btn btn-primary">{{ artist.name }}</router-link>
        </li>
      </ol>
    </div>

    <div>
      <h5>Songs in <span class="font-italic">{{ album.album_name }}</span>:</h5>
      <ol>
        <li v-for="song in album.songs" :key="song.id" class="mb-4">
          <router-link :to="'/songinfo/' + song.id" class="btn btn-secondary">{{ song.name }}</router-link>
          <audio :src="'http://127.0.0.1:5000/' + song.path" class="ml-3" controls></audio>
        </li>
      </ol>
    </div>
  </div>
</template>

  
  <script>
  export default {
    data() {
      return {
        album: {
            'album_id': '',
            'album_name': '',
            'rcount': 0,
            'artists':[],
            'songs':[]
        },
        user_id: parseInt(localStorage.userId)
      };
    },
    mounted() {
      this.checkUser();
      this.fetchAlbum();
    },
    methods: {
      checkUser(){
        if (!localStorage.token) {
          alert("Login again")
          this.$router.push('/login');
        }
        fetch('http://127.0.0.1:5000/jwt/testing', {
          method: 'GET',
          headers: {
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
      },
      fetchAlbum() {
        const albumId = parseInt(this.$route.params.albumId);
        fetch(`http://127.0.0.1:5000/albums/${albumId}`,{
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.token}`
          }
          })
          .then(response => response.json())
          .then(data => {
            this.album = data; 
          })
          .catch(error => {
            console.error('Error fetching album data:', error);
          });
      }
    }
  };
  </script>
  
<style scoped>

</style>
  