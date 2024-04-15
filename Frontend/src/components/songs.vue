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
    <div class="sorting-buttons">
      <button @click="sortByRating" class="btn btn-primary">Top Rated</button>
      <button @click="sortByPlaycount" class="btn btn-primary">Most Played</button>
      <button @click="sortByRecent" class="btn btn-primary">Most Recent</button>
    </div>
    <section>
      <div class="card">
        <ol id="songList">
          <li v-for="song in filteredSongs" :key="song.song_id" class="song-entry">
            <div class="song-details">
              <h5 class="song-title card-header">{{ song.song_name }}</h5>
              <div class="card-body">
                <p class="card-text">
                  <h6 style="display: inline;">Genre :</h6>{{ song.song_genre }} <br>
                  <h6 style="display: inline;">Artists : </h6> 
                  <span v-for="artist in song.artists" :key="artist.artist_id">{{ artist.name }}</span> <br>
                  <h6 style="display: inline;">Albums : </h6>
                  <span v-for="album in song.albums" :key="album.album_id">{{ album.name}}</span>
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
    data() {
      return {
        searchQuery: '',
        songs: [],
        filteredSongs: [],
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
        if (!localStorage.token) {
          this.$router.push('/login');
          return; 
        }
        fetch('http://127.0.0.1:5000/songs/0', {
          method:"GET",
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
          this.songs = [...data].sort((a, b) => b.pcount - a.pcount).reverse();
          this.filteredSongs=this.songs;
        })
        .catch(error => {
          console.error('Error fetching songs:', error);
          this.$router.push('/login');
        });
      },
      search() {
        const query = this.searchQuery.toLowerCase();
        this.filteredSongs = this.songs.filter(song =>
          song.song_name.toLowerCase().includes(query)
        );
      },
      sortByRating() {
        this.filteredSongs = [...this.songs].sort((a, b) => b.rating - a.rating);
      },
      sortByPlaycount() {
        this.filteredSongs = [...this.songs].sort((a, b) => b.pcount - a.pcount);
      },
      sortByRecent() {
        this.filteredSongs = [...this.songs].sort((a, b) =>  new Date(b.created_at) - new Date(a.created_at));
      },
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
  