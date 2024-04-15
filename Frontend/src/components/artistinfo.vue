<template>
  <div class="container">
    <h2 class="text-center mt-5 mb-4">{{ artist.artist_name }}</h2>

    <div class="mb-5">
      <h5>Albums by <span class="font-italic">{{ artist.artist_name }}</span>:</h5>
      <ol class="list-group">
        <li v-for="album in artist.albums" :key="album.id" class="list-group-item">
          <router-link :to="'/albums/' + album.id" class="btn btn-primary btn-block btn-lg">{{ album.name }}</router-link>
        </li>
      </ol>
    </div>

    <div>
      <h5>Songs by <span class="font-italic">{{ artist.artist_name }}</span>:</h5>
      <ol>
        <li v-for="song in artist.songs" :key="song.id" class="mb-4">
          <router-link :to="'/songinfo/' + song.id" class="btn btn-info btn-block btn-lg">{{ song.name }}</router-link><br>
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
      this.checkUser();
      this.fetchArtist();
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
      fetchArtist() {
        const artistId = parseInt(this.$route.params.artistId);
        fetch(`http://127.0.0.1:5000/artists/${artistId}`,{
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.token}`
          }
          })
          .then(response => response.json())
          .then(data => {
            this.artist = data;
          })
          .catch(error => {
            console.error('Error fetching artist data:', error);
          });
      }
    }
  };
  </script>
  
<style scoped>

</style>
  