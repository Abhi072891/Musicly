<template>
  <div class="song-details">
    <h5 class="song-title">{{ song.song_name }}</h5>
    <p>
      Genre: 
      <router-link :to="'/genre/' + song.song_genre" class="btn btn-primary" v-if="song.song_genre">
        {{ song.song_genre }}
      </router-link>
    </p>

    <p>
      Artists:
      <template v-for="(artist, index) in song.artists">
        <router-link :to="'/artists/' + artist.id" class="btn btn-primary">{{ artist.name }}</router-link>
        <span v-if="index < song.artists.length - 1">, </span>
      </template>
    </p>

    <p>
      Albums:
      <template v-for="(album, index) in song.albums">
        <router-link :to="'/albums/' + album.id" class="btn btn-primary">{{ album.name }}</router-link>
        <span v-if="index < song.albums.length - 1">, </span>
      </template>
    </p>

    <p>Rating: {{ song.rating }}</p>

    <p v-if="rated">You rated this song: {{ ratevalue }}/5</p>

    <div class="btn-group">
      <button class="btn btn-primary" @click="play"><img src="/play.png" alt="Play"></button>
      <!-- <button class="btn btn-primary" @click="play">Play</button> -->
      <button class="btn btn-secondary" @click="showLyrics">Lyrics</button>
      <button class="btn btn-secondary" @click="showRating">Rate</button>
      <button class="btn btn-secondary" @click="addToPlaylist">Add to playlist</button>
    </div>

    <audio :src="'http://127.0.0.1:5000/' + song.song_path" id="player" style="display: none; width: 100%;" controls></audio>

    <form v-if="showAddToPlaylist" @submit.prevent="addToPlaylistSubmit">
      <label for="playlist_id">Select a Playlist:</label>
      <select v-model="selectedPlaylistId" required @change="handlePlaylistChange" class="form-control">
        <option value="" disabled>Select a Playlist</option>
        <option v-for="playlist in playlists" :value="playlist.playlist_id" :key="playlist.playlist_id">{{ playlist.playlist_name }}</option>
        <option value="new">Create a New playlist</option>
      </select>
      <input type="text" v-model="newPlaylistName" v-if="creatingNewPlaylist" placeholder="Give Name for Playlist" class="form-control">
      <button type="submit" class="btn btn-light mt-2">Done</button>
    </form>

    <div class="song-actions" v-if="showRateSection">
      <p v-if="rated">Want to rate this song again?</p>
      <form @submit.prevent="submitRating">
        <div class="rating">
          <p>Rate the Song:</p>
          <label v-for="star in stars" :key="star" :title="star + ' stars'">
            {{ star }}
            <input type="radio" v-model="rating" :value="star" :id="'star' + star">
          </label>
          <button type="submit" class="btn btn-primary">Rate</button>
        </div>
      </form>
    </div>

    <p v-if="showlyrics" class="lyrics text-center">{{ song.song_lyrics }}</p>
  </div>
</template>

<script>
export default {
  props: {
    songId: {
      required: true,
    },
  },
  data() {
    return {
      song: {
        "song_id": 0,
        "song_name": "",
        "song_genre": "",
        "song_lyrics": "",
        "song_path": "",
        "rating": 0,
        "pcount": 0,
        "albums": [],
        "artists": []
      },
      user_id: localStorage.user_id,
      rated: false,
      ratevalue: null,
      playlists: [],
      showAddToPlaylist: false,
      selectedPlaylistId: '',
      creatingNewPlaylist: false,
      newPlaylistName: '',
      showRateSection: false,
      stars: [1, 2, 3, 4, 5],
      rating: null,
      showlyrics: false
    };
  },
  mounted() {
    this.fetchSongData();
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
    play() {
      let player = document.getElementById('player');
      player.style.display = 'block';
    },
    showRating() {
      this.showRateSection = true;
    },
    showLyrics() {
      this.showlyrics = true;
    },
    addToPlaylist() {
      this.showAddToPlaylist = true;
    },

    handlePlaylistChange() {
      if (this.selectedPlaylistId === 'new') {
        this.creatingNewPlaylist = true;
      } else {
        this.creatingNewPlaylist = false;
      }
    },
    addToPlaylistSubmit() {

      if (this.creatingNewPlaylist) {
        fetch(`http://127.0.0.1:5000/playlists/${parseInt(this.user_id)}`, {
          method: 'POST',
          body: JSON.stringify({
            "playlist_id": "new",
            "new_playlist_name": `${this.newPlaylistName}`,
            "song_ids": [parseInt(this.songId)]
          }),
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
          }).then(data => {
            console.log(data)
          })
          .catch(error => {
            console.log(error)
          })
      } else {
        fetch(`http://127.0.0.1:5000/addsongtopl/${parseInt(this.selectedPlaylistId)}/${parseInt(this.songId)}`, {
          method: 'GET',
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
          }).then(data => {
            console.log(data)
            alert("song added to playlist")
            window.location.reload()

          })
          .catch(error => {
            console.log(error)
          })
      }
    },
    submitRating() {
      // Handle rating submission
      if (Number.isInteger(this.rating)) {
        fetch(`http://127.0.0.1:5000/rating/${parseInt(this.songId)}/${parseInt(this.user_id)}`, {
          method: 'POST',
          body: JSON.stringify({ 'rating': parseInt(this.rating) }),
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
          }).then(data => {
            console.log(data)
            this.fetchSongData()
          })
          .catch(error => {
            console.log(error)
          })
      }
    },
    fetchSongData() {
      // Fetch song data using songId
      fetch(`http://127.0.0.1:5000/songs/${parseInt(this.songId)}`, {
        method: "GET",
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.token}`
        }
      })
        .then(response => response.json())
        .then(data => {
          this.song = data; // Assuming the response contains song details
        })
        .catch(error => {
          console.error('Error fetching song data:', error);
        });
      // Fetch user's playlists
      fetch(`http://127.0.0.1:5000/playlists/${parseInt(this.user_id)}/0`, {
        method: "GET",
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.token}`
        }
      })
        .then(response => response.json())
        .then(data => {
          this.playlists = data; 
        })
        .catch(error => {
          console.error('Error fetching user playlists:', error);
        });
      // Fetch user's rating for the song
      fetch(`http://127.0.0.1:5000/rating/${parseInt(this.songId)}/${parseInt(this.user_id)}`, {
        method: "GET",
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

          this.rated = true
          this.ratevalue = parseInt(data.ratevalue);

        })
        .catch(error => {
          console.error('Error fetching user rating for the song:', error);
        });

    },
  },
};
</script>

<style scoped>
  .song-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 10px;
  }

  .song-details {
    font-size: 16px;
    color: #333;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }

  .rating label {
    font-size: 18px;
    color: #ffac42;
  }

  .btn-group {
    margin-top: 20px;
  }

  .form-control {
    margin-top: 10px;
  }

  .lyrics {
    color: darkgreen;
    font-size: 18px;
    font-weight: 600;
    margin-top: 20px;
  }
</style>