<template>
    <section class="search-bar py-4">
      <div class="container">
        <div class="row">
          <div class="col-md-8 offset-md-2">
            <div class="input-group">
              <input type="text" class="form-control" v-model="searchQuery" placeholder="Search for song...">
              <button class="btn btn-primary" type="button" @click="search">Search</button>
            </div>
          </div>
        </div>
      </div>
    </section>
    <section>
        <h3 style="text-align: center; color: blueviolet;">Genre : {{ this.genre }}</h3> <br>
      <div class="card">
        <ol id="songList">
          <li v-for="song in filteredSongs" :key="song.song_id" class="song-entry">
            <div class="song-details">
              <h5 class="song-title card-header">{{ song.song_name }}</h5>
              <div class="card-body">
                <p class="card-text">
                  <h6 style="display: inline;">Artists : </h6> 
                  <span v-for="artist in song.artists" :key="artist.artist_id">{{ artist.artist_id }}</span> <br>
                  <h6 style="display: inline;">Albums : </h6>
                  <span v-for="album in song.albums" :key="album.album_id">{{ album.album_id }}</span>
                  <router-link :to="'/songinfo/' + song.song_id " class="btn btn-primary" style="margin-left: 500px;">Go to Song</router-link>
                </p>
              </div>
              Rating : {{ song.rating }}
            </div>
          </li>
        </ol>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    props: {
        genre: {
        type: String,
        required: true
        }
    },
    data() {
      return {
        searchQuery: '',
        songs: [],
      };
    },
    mounted() {
      this.fetchSongs();
      this.checkUser();
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
      fetchSongs() {
        fetch(`http://127.0.0.1:5000/genre/${this.genre}`,{
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
      search() {
        const query = this.searchQuery.toLowerCase();
        this.filteredSongs = this.songs.filter(song =>
          song.song_name.toLowerCase().includes(query)
        );
      }
    },
    computed: {
      filteredSongs() {
        const query = this.searchQuery.toLowerCase();
        return this.songs.filter(song =>
          song.song_name.toLowerCase().includes(query)
        );
      }
    },
  };
  </script>
  
  <style scoped>
  .song-entry {
    justify-content: space-between;
    padding: 20px;
    margin: 10px 0;
    background-color: #f8f8f8;
    border-radius: 8px;
    font-family: 'Poppins', sans-serif;
  }
  .song-title {
    font-size: 20px;
    font-weight: bold;
  }
  .song-details {
    font-size: 14px;
    color: #888;
  }
  </style>
  