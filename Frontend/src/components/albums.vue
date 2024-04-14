<template>
    <section class="search-bar py-4">
      <div class="container">
        <div class="row">
          <div class="col-md-8 offset-md-2">
            <div class="input-group">
              <input type="text" class="form-control" v-model="searchQuery" placeholder="Search for Album...">
              <button class="btn btn-primary" type="button" @click="search">Search</button>
            </div>
          </div>
        </div>
      </div>
    </section>
  
    <div class="container">
      <div class="row">
        <div class="col-md-4" v-for="album in filteredAlbums" :key="album.album_id">
          <div class="card" style="width: 18rem;">
            <img class="card-img-top" src="/album.jpg" alt="Album">
            <div class="card-body">
              <h5 class="card-title title">{{ album.album_name }}</h5>
              <h6 style="display: inline;">Artists : </h6>
              <p v-for="(artist, index) in album.artists" :key="index" class="card-text" style="display: inline;">{{ artist.name }}{{ index < album.artists.length - 1 ? ', ' : '' }}</p>
              <br>
              <h6 >Songs : </h6>             
              <div v-if="album.songs.length > 0">
                <ol>
                    <template v-if="album.songs.length <= 5">
                        <li v-for="(song, index) in album.songs" :key="index">
                            {{ song.name }}
                        </li>
                    </template>
                    <template v-else>
                        <li v-for="(song, index) in album.songs.slice(0, 5)" :key="index">
                            {{ song.name }}
                        </li>
                    </template>
                </ol>
            </div>
              
              <br><br>
              <router-link :to="'/albums/' + album.album_id" class="btn btn-primary">Go to Album</router-link>
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
        searchQuery: '',
        albums: [],
        user_id: localStorage.user_id
      };
    },
    mounted() {
      this.checkUser();
      this.fetchAlbums();
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
      fetchAlbums() {
        // Perform fetch request to get albums data
        fetch(`http://127.0.0.1:5000/albums/0`,{
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.token}`
          }
          })
          .then(response => response.json())
          .then(data => {
            this.albums = data; // Set fetched albums data
          })
          .catch(error => {
            console.error('Error fetching albums data:', error);
          });
      },
      search() {
        const query = this.searchQuery.toLowerCase();
        return this.albums.filter(album =>
          album.album_name.toLowerCase().includes(query)
        );
      }
    },
    computed: {
      filteredAlbums() {
        const query = this.searchQuery.toLowerCase();
        return this.albums.filter(album =>
          album.album_name.toLowerCase().includes(query)
        );
      }
    },
  };
  </script>
  
  <style scoped>
  /* Add your scoped styles here */
  </style>
  