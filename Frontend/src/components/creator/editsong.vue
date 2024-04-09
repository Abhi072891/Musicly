<template>
    <div class="container">
      <h1 style="color: #0056b3;">Edit Song</h1>
      <router-link :to="'/creator'" class="btn btn-secondary">Go back</router-link>
      <form @submit.prevent="updateSong">
        <div class="form-group">
          <label for="songName" class="required">Song Name:</label>
          <input type="text" id="songName" v-model="editedSong.songname" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="artistNames">Name of Artists (Comma Separated):</label>
          <input type="text" id="artistNames" v-model="artistNames" class="form-control">
        </div>
        <div class="form-group">
          <label for="genre">Genres:</label>
          <select id="genre" v-model="editedSong.genre" class="form-control">
            <option v-for="genre in genres" :key="genre" :value="genre">{{ genre }}</option>
          </select>
        </div>
        <div class="form-group">
          <label for="album">Album:</label>
          <select id="album" v-model="editedSong.album" class="form-control" @change="toggleNewAlbumInput" required>
            <option value="nochange">No Change</option>
            <option value="none">None</option>
            <option value="new">Create a New Album</option>
            <option v-for="album in albums" :key="album.album_id" :value="album.album_name">{{ album.album_name }}</option>
          </select>
          <input type="text" v-if="editedSong.album === 'new'" v-model="newAlbumName" placeholder="Enter New Album Name" class="form-control">
        </div>
        <div class="form-group">
          <label for="songLyrics">Lyrics:</label>
          <textarea id="songLyrics" v-model="editedSong.lyrics" class="form-control" rows="4"></textarea>
        </div>
        <div class="form-group">
          <button type="submit" class="btn btn-primary">Update Song</button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        user_id: parseInt(localStorage.user_id),
        editedSong: {
          songname: '',
          genre: '',
          album: 'nochange',
          lyrics: ''
        },
        artistNames: '',
        genres: ['Pop', 'Rock', 'Hip-Hop', 'Jazz', 'Country', 'Electronic', 'R&B', 'Reggae', 'Classical', 'Blues', 'Metal', 'Alternative', 'Indie', 'Folk', 'Punk', 'Other'],
        albums: [], 
        newAlbumName: '' 
      };
    },
    mounted() {
      this.fetchSongDetails();
      this.fetchAlbums();
    },
    methods: {
      fetchSongDetails() {
        const song_id = parseInt(this.$route.params.songId);
        fetch(`http://127.0.0.1:5000/songs/${song_id}`)
          .then(response => response.json())
          .then(data => {
            this.editedSong.songname = data.song_name;
            this.editedSong.genre = data.song_genre;
            this.artistNames = data.artists.map(artist => artist.name).join(', ');
            this.editedSong.album = data.album;
            this.editedSong.lyrics = data.song_lyrics;
          })
          .catch(error => console.error('Error fetching song details:', error));
      },
      fetchAlbums() {
        // Fetch albums for the dropdown
        fetch(`http://127.0.0.1:5000/albumsbyuser/${this.user_id}`)
          .then(response => response.json())
          .then(data => {
            this.albums = data;
          })
          .catch(error => console.error('Error fetching albums:', error));
      },
      toggleNewAlbumInput() {
        // Toggle display of the new album input field
        if (this.editedSong.album === 'new') {
          this.newAlbumName = ''; // Clear input field
        }
      },
      updateSong() {
        const formData = {
          songname: this.editedSong.songname,
          artistname: this.artistNames,
          genre: this.editedSong.genre,
          album: this.editedSong.album,
          new_album_name: this.newAlbumName,
          lyrics: this.editedSong.lyrics
        };
  
        const song_id = this.$route.params.songId;
        fetch(`http://127.0.0.1:5000/songs/${this.user_id}/${song_id}`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(formData)
        })
        .then(response => {
          if (response.ok) {
            alert("Song updated successfully")
            this.$router.push(`/creator`);
          } else {
            console.error('Error updating song');
          }
        })
        .catch(error => console.error('Error updating song:', error));
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add component-specific styles here */
  </style>
  