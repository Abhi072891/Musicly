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
            <!-- <img class="card-img-top" src="/static/album.jpg" alt="Album"> -->
            <img class="card-img-top" src="" alt="Album">
            <div class="card-body">
              <h5 class="card-title title">{{ album.album_name }}</h5>
              <h6 style="display: inline;">Artists : </h6>
              <p v-for="(artist, index) in album.artists" :key="index" class="card-text" style="display: inline;">{{ artist.name }}{{ index < album.artists.length - 1 ? ', ' : '' }}</p>
              <br>
              <h6 >Songs : </h6>
              <!-- <p v-for="(song, index) in album.songs" :key="index" class="card-text">{{ song.song_name }}</p> -->
              
            <div v-if="album.songs.length > 0">
                <h5>Songs in {{ album.album_name }}:</h5>
                <ol>
                    <template v-if="album.songs.length <= 5">
                        <li v-for="(song, index) in album.songs" :key="index">
                            <!-- <a href="/songinfo/{{ song.song_id }}/{{ user_id }}">{{ song.song_name }}</a>
                            <br><audio :src="'/' + song.song_path" controls></audio> -->
                            {{ song.name }}
                        </li>
                    </template>
                    <template v-else>
                        <li v-for="(song, index) in album.songs.slice(0, 5)" :key="index">
                            <!-- <a href="/songinfo/{{ song.song_id }}/{{ user_id }}">{{ song.song_name }}</a>
                            <br><audio :src="'/' + song.song_path" controls></audio> -->
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
      // Fetch albums data
      this.fetchAlbums();
    },
    methods: {
      fetchAlbums() {
        // Perform fetch request to get albums data
        fetch(`http://127.0.0.1:5000/albums/0`)
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
  