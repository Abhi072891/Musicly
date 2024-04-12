<template>
    <div class="container">
      <h1>Creator Dashboard</h1>
  
      <!-- Create Song and Album Buttons -->
      <div class="mb-4">
        <button @click="createSong" class="btn btn-primary mr-2">Create Song</button>
        <button @click="createAlbum" class="btn btn-primary">Create Album</button>
      </div>
  
      <!-- List of Albums -->
      <div v-if="albums.length > 0">
        <h2>Albums Created : {{ albums.length }}</h2>
        <ul class="list-group">
          <li v-for="album in albums" :key="album.album_id" class="list-group-item">
            <div class="d-flex justify-content-between align-items-center">
            <span>{{ album.album_name }}</span>
            <div class="btn-group ml-2">
              <button @click="editAlbum(album.album_id)" class="btn btn-info">Edit</button>
              <button @click="deleteAlbum(album.album_id)" class="btn btn-danger">Delete</button>
              <router-link :to="'/albums/' + album.album_id" class="btn btn-primary">Go to Album</router-link>
            </div>
            </div>
          </li>
        </ul>
      </div>
  
      <!-- List of Songs -->
      <div v-if="songs.length > 0">
        <h2>Songs Created : {{ songs.length }}</h2>
        <ul class="list-group">
            <li v-for="song in songs" :key="song.song_id" class="list-group-item">
                <div class="d-flex justify-content-between align-items-center">
                <span>{{ song.song_name }}</span>
                <div class="btn-group">
                    <button @click="editSong(song.song_id)" class="btn btn-info">Edit</button>
                    <button @click="deleteSong(song.song_id)" class="btn btn-danger">Delete</button>
                    <router-link :to="'/songinfo/' + song.song_id" class="btn btn-primary">Go to Song</router-link>
                </div>
                </div>
            </li>
        </ul>

      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        albums: [],
        songs: [],
        creatorId: parseInt(localStorage.user_id)
      };
    },
    mounted() {
      this.checkUserRole();
      this.fetchAlbums();
      this.fetchSongs();
    },
    methods: {
      checkUserRole() {
      // Check if the role is 'user' in localStorage
      const role = localStorage.getItem('user_role');
      const status = localStorage.getItem('status');
      if(role==='admin'){
        this.$router.push('/admindashboard');
      }
      
      if (status === 'wait') {
        // Alert the user that the application is under process
        alert('Your application is under process. Please wait for approval.');
        // Redirect to home
        this.$router.push('/home');
      } else if(status=='blc'){
          alert("You have been Blacklisted from being a creator")
          this.$router.push('/home')
      } else if (role === 'user') {
        // Prompt the user to become a creator
        const confirmPrompt = confirm('Would you like to become a creator?');
        if (confirmPrompt) {
          // Redirect to application form
          this.$router.push('/creator-application');
        } else {
          // Redirect to home
          this.$router.push('/home');
        }
      }
    },
      fetchAlbums() {
        fetch(`http://127.0.0.1:5000/albumsbyuser/${this.creatorId}`)
        .then(respose => respose.json())
        .then(data => {
            this.albums=data
        })
        .catch(error => console.log(error))
      },
      fetchSongs() {
        fetch(`http://127.0.0.1:5000/songsbyuser/${this.creatorId}`)
        .then(respose => respose.json())
        .then(data => {
            this.songs=data
        })
        .catch(error => console.log(error))
      },
      createSong() {
        // Redirect to create song page
        this.$router.push('/songupload');
      },
      createAlbum() {
        // Redirect to create album page
        this.$router.push('/createalbum');
      },
      editSong(songId) {
        // Redirect to edit song page
        this.$router.push(`/editsong/${songId}`);
      },
      editAlbum(albumId) {
        // Redirect to edit album page
        this.$router.push(`/editalbum/${albumId}`);
      },
      deleteSong(songId) {
        if (confirm("Are you sure you want to delete this song?")) {
            fetch(`http://127.0.0.1:5000/songs/${parseInt(songId)}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Song deleted successfully:', data);
                alert("Song deleted successfully");
                    setTimeout(() => {
                        location.reload();
                    }, 1000);
            })
            .catch(error => {
                console.error('Error deleting song:', error);
            });
        }
      },
      deleteAlbum(albumId) {
        if (confirm("Are you sure you want to delete this album?")) {
            fetch(`http://127.0.0.1:5000/albums/${parseInt(albumId)}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    // 'Authorization': `Bearer ${localStorage.token}` 
                }
            })
            .then(response => {
                if (response.ok) {
                    alert("Album deleted successfully");
                    // window.location.reload()
                    setTimeout(() => {
                        location.reload();
                    }, 1000);
                } else {
                    alert("Failed to delete album");
                }
            })
            .catch(error => {
                console.error('Error deleting album:', error);
                alert("Failed to delete album");
            });
        }
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add your component-specific styles here */
  </style>
  