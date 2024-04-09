<template>
    <div class="container">
  
        <div class="top-section">
            <h2>Most Played Songs</h2>
            <div class="row">
                <div v-for="(song, index) in sortedSongsByRating" :key="song.song_id" class="col-md-3" >
                    <div class="card">
                        <h5 class="song-title card-header">{{ song.song_name }}</h5>
                        <p class="card-text">
                            <h6 style="display: inline;">Genre :</h6>{{ song.song_genre }} <br>                   
                            Rating : {{ song.rating }}
                        </p>
                        <div class="card-footer">
                            <router-link to="'/songinfo/' + song.song_id " class="btn btn-primary" style="margin-left: 30px;">Go to Song</router-link>
                        </div>
                    </div>
                </div>
            </div>
            <router-link to="/songs" class="btn btn-primary">More</router-link>
        </div>
  
        <div class="top-section">
            <h2>Top Songs by Rating</h2>
            <div class="row">
                <div v-for="(song, index) in sortedSongsByRating" :key="song.song_id" class="col-md-3" >
                    <div class="card">
                        <h5 class="song-title card-header">{{ song.song_name }}</h5>
                        <p class="card-text">
                            <h6 style="display: inline;">Genre :</h6>{{ song.song_genre }} <br>                   
                            Rating : {{ song.rating }}
                        </p>
                        <div class="card-footer">
                            <router-link to="'/songinfo/' + song.song_id " class="btn btn-primary" style="margin-left: 30px;">Go to Song</router-link>
                        </div>
                    </div>
                </div>
            </div>
            <router-link to="/songs" class="btn btn-primary">More</router-link>
        </div>
    
        <div class="top-section">
            <h2>Top Albums</h2>
            <div class="row">
                <div v-for="(album, index) in topAlbumsBySeenCount" :key="album.id" class="col-md-3">
                    <div class="card">
                        <h5 class="song-title card-header">{{ album.album_name }}</h5>
                        <h6 >Artists : </h6>
                        <p v-for="(artist, index) in album.artists" :key="index" class="card-text" style="display: inline;">{{ artist.name }}{{ index < album.artists.length - 1 ? ', ' : '' }}</p>
                        <div class="card-footer">
                            <router-link :to="'/albuminfo/' + album.album_id " class="btn btn-primary" style="margin-left: 30px;">Go to Album</router-link>
                        </div>
                    </div>
                </div>
            </div>
            <router-link to="/albums" class="btn btn-primary">More</router-link>
        </div>

        <div class="top-section">
            <h2>Top Artists</h2>
            <div class="row">
                <div v-for="(artist, index) in topArtistsBySeenCount" :key="artist.id" class="col-md-3">
                    <div class="card">
                        <h5 class="song-title card-header">{{ artist.artist_name }}</h5>
                        <h6 >Albums : </h6>
                        <p v-for="(album, index) in artist.albums" :key="index" class="card-text" style="display: inline;">{{ album.name }}{{ index < artist.albums.length - 1 ? ', ' : '' }}</p>
                        <div class="card-footer">
                            <router-link :to="'/artistinfo/' + artist.artist_id " class="btn btn-primary" style="margin-left: 30px;">Go to Artist</router-link>
                        </div>
                    </div>
                </div>
            </div>
            <router-link to="/artists" class="btn btn-primary">More</router-link>
        </div>
  
      
  
      <div class="genres-section">
        <h2>All Genres</h2>
        <div class="row">
          <div v-for="genre in allGenres" :key="genre" class="list-group-item col-md-3" style="padding: 5px; margin: 5px;"><router-link :to="'/genre/'+ genre " class="btn btn-secondary">{{ genre }}</router-link> </div>
        </div>
      </div>
  
    </div>
</template>
  
  <script>
  export default {
    data() {
      return {
        topAlbumsBySeenCount: [],
        topArtistsBySeenCount: [],
        allGenres:['Pop', 'Rock', 'Hip-Hop', 'Jazz', 'Country', 'Electronic', 'R&B', 'Reggae', 'Classical', 'Blues', 'Metal', 'Alternative', 'Indie', 'Folk', 'Punk', 'Other'],
        allsongs:[],
        sortedSongsByPlaycount:[],
        sortedSongsByRating:[],
      };
    },
    mounted() {
      this.fetchSongs();
      this.fetchAlbums();
      this.fetchArtists();
    },
    methods: {
      fetchSongs() {
        // if (!localStorage.token) {
        //   this.$router.push('/login');
        //   return; 
        // }
        fetch('http://127.0.0.1:5000/songs/0', {
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
          this.allsongs = data;
          this.sortByPlaycount();
          this.sortByRating();
        })
        .catch(error => {
          console.error('Error fetching songs:', error);
          this.$router.push('/login');
        });
        },
        sortByRating() {
          // Sort songs by rating in descending order
          this.sortedSongsByRating = [...this.allsongs].sort((a, b) => b.rating - a.rating);
        },
        sortByPlaycount() {
          // Sort songs by playcount in descending order
          this.sortedSongsByPlaycount = [...this.allsongs].sort((a, b) => b.pcount - a.pcount);
        },
        fetchAlbums() {
            fetch(`http://127.0.0.1:5000/albums/0`)
            .then(response => response.json())
            .then(data => {
                // this.albums = data; // Set fetched albums data
                this.topAlbumsBySeenCount= [...data].sort((a, b) => b.pcount - a.pcount);
            })
            .catch(error => {
                console.error('Error fetching albums data:', error);
            });
        },
        fetchArtists() {
            fetch(`http://127.0.0.1:5000/artists/0`)
            .then(response => response.json())
            .then(data => {
                // this.albums = data; // Set fetched albums data
                this.topArtistsBySeenCount= [...data].sort((a, b) => b.pcount - a.pcount);
            })
            .catch(error => {
                console.error('Error fetching albums data:', error);
            });
        },
    },
  };
  </script>
  
  <style scoped>
  .container {
    padding: 20px;
  }
  
  .top-section {
    margin-bottom: 30px;
  }
  
  .create-playlist-section {
    text-align: center;
    margin-top: 50px;
  }

  </style>
  
  