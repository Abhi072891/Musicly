<template>
    <div class="container">
      <h2 style="text-align: center; margin: 50px;"> {{ album.album_name }} </h2>
      <br>
      
      <h5>Artists of Album {{ album.album_name }}: </h5>
      <ol>
        <li v-for="artist in album.artists" :key="artist.id">
          <router-link :to="'/artists/' + artist.id">{{ artist.name }}</router-link>
            <!-- {{ artist.name }} -->
        </li>
      </ol>
      <br><br>
  
      <h5>Songs in {{ album.album_name }}: </h5>
      <ol>
        <li v-for="song in album.songs" :key="song.id">
          <router-link :to="'/songinfo/' + song.id">{{ song.name }}</router-link>
          <!-- {{ song.name }} -->
          <!-- <br><audio :src="'/' + song.song_path" controls></audio> -->
          <br><audio :src="'http://127.0.0.1:5000/' + song.path" style="width: 600px;"controls></audio>
        </li>
      </ol>
      <br>
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
      // Fetch album data
      this.fetchAlbum();
    },
    methods: {
      fetchAlbum() {
        // Extract album_id and user_id from route params
        const albumId = parseInt(this.$route.params.albumId);
        // const userId = this.$route.params.user_id;
  
        // Perform fetch request to get album data
        fetch(`http://127.0.0.1:5000/albums/${albumId}`)
          .then(response => response.json())
          .then(data => {
            this.album = data; // Set fetched album data
          })
          .catch(error => {
            console.error('Error fetching album data:', error);
          });
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add your scoped styles here */
  </style>
  