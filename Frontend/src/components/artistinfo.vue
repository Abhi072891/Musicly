<template>
    <div class="container">
      <h2 style="text-align: center; margin: 50px;"> {{ artist.artist_name }} </h2>
      <br>
      
      <h5>Albums by {{ artist.artist_name }}: </h5>
      <ol>
        <li v-for="album in artist.albums" :key="album.id">
          <router-link :to="'/albums/' + album.id">{{ album.name }}</router-link>
            <!-- {{  album.name }} -->
        </li>
      </ol>
      <br><br>
  
      <h5>Songs by {{ artist.artist_name }}: </h5>
      <ol>
        <li v-for="song in artist.songs" :key="song.id">
            <!-- {{ song.name }} -->
          <router-link :to="'/songinfo/' + song.id">{{ song.name }}</router-link>
          <!-- <br><audio :src="'/' + song.song_path" controls></audio> -->
          <audio :src="'http://127.0.0.1:5000/' + song.path" style="width: 600px;"controls></audio>
        </li>
      </ol>
      <br>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        artist: {
            'artist_id': '',
            'artist_name': '',
            'scount': 0,
            'albums':[],
            'songs':[]
        },
        user_id: parseInt(localStorage.user_id)
      };
    },
    mounted() {
      // Fetch artist data
      this.fetchArtist();
    },
    methods: {
      fetchArtist() {
        // Extract artist_id and user_id from route params
        const artistId = parseInt(this.$route.params.artistId);
        // const userId = this.$route.params.user_id;
  
        // Perform fetch request to get artist data
        fetch(`http://127.0.0.1:5000/artists/${artistId}`)
          .then(response => response.json())
          .then(data => {
            this.artist = data; // Set fetched artist data
          })
          .catch(error => {
            console.error('Error fetching artist data:', error);
          });
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add your scoped styles here */
  </style>
  