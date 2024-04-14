<template>
    <section class="search-bar py-4">
      <div class="container">
        <div class="row">
          <div class="col-md-8 offset-md-2">
            <div class="input-group">
              <input type="text" class="form-control" v-model="searchQuery" placeholder="Search for Artist...">
              <button class="btn btn-primary" type="button" @click="search">Search</button>
            </div>
          </div>
        </div>
      </div>
    </section>
  
    <div class="container">
      <div class="row">
        <div class="col-md-4" v-for="artist in filteredArtists" :key="artist.artist_id">
          <div class="card" style="width: 18rem;" v-if="artist.songs.length > 0">
            <img class="card-img-top" src="/artist.jpg" alt="Artist">
            <div class="card-body">
              <h5 class="card-title title">{{ artist.artist_name }}</h5>
              <h6 style="display: inline;">Albums : </h6>
              <p v-for="(album, index) in artist.albums" :key="index" class="card-text" style="display: inline;">{{ album.name }}{{ index < artist.albums.length - 1 ? ', ' : '' }}</p>
              <br>

            <div v-if="artist.songs.length > 0">
              <h5>Songs by {{ artist.artist_name }}:</h5>
              <ol>
                <template v-if="artist.songs.length <= 5">
                  <li v-for="(song, index) in artist.songs" :key="index">
                      {{ song.name }}
                  </li>
                </template>
                <template v-else>
                  <li v-for="(song, index) in artist.songs.slice(0, 5)" :key="index">
                      {{ song.name }}
                  </li>
                </template>
              </ol>
            </div>
              <br><br>
              <router-link :to="'/artists/' + artist.artist_id" class="btn btn-primary">Go to Artist</router-link>
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
        artists: [],
      };
    },
    mounted() {
      this.checkUser();
      this.fetchArtists();
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
      fetchArtists() {
        // Perform fetch request to get artists data
        fetch(`http://127.0.0.1:5000/artists/0`,{
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.token}`
          }
          })
          .then(response => response.json())
          .then(data => {
            this.artists = data; // Set fetched artists data
          })
          .catch(error => {
            console.error('Error fetching artists data:', error);
          });
      },
      search() {
        const query = this.searchQuery.toLowerCase();
        return this.artists.filter(artist =>
          artist.artist_name.toLowerCase().includes(query)
        );
      }
    },
    computed: {
      filteredArtists() {
        const query = this.searchQuery.toLowerCase();
        return this.artists.filter(artist =>
          artist.artist_name.toLowerCase().includes(query)
        );
      }
    },
  };
  </script>
  
  <style scoped>
  /* Add your scoped styles here */
  </style>
  