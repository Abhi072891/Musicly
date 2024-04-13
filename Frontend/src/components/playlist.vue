<template>
    <div class="container mt-5">
      <h1>Playlists</h1>
  
      <!-- Create Playlist Form -->
      <form @submit.prevent="createPlaylist" class="mb-4">
        <div class="form-group">
          <label for="playlistName">Create Playlist:</label>
          <input type="text" id="playlistName" v-model="newPlaylistName" required class="form-control">
        </div>
        <button type="submit" class="btn btn-primary">Create</button>
      </form>
  
      <div>
        <h2>Your Playlists:</h2>
        <ul class="list-group">
            <li v-for="playlist in playlists" :key="playlist.playlist_id" class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                    <button @click="showPlaylist(playlist.playlist_id, playlist.playlist_name)" class="btn btn-primary">{{ playlist.playlist_name }}</button>
                </div>
                <div>
                    <button @click="deletePlaylist(playlist.playlist_id)" class="btn btn-danger">Delete this playlist</button>
                </div>
            </li>
        </ul>
      </div>
  
      <!-- Show Playlist Songs -->
      <div v-if="showPlaylisttoggle" class="mt-4">
        <h2>{{ currentPlaylistName }} Songs:</h2>
        <ul class="list-group">
          <li v-for="song in currentPlaylist" :key="song.id" class="list-group-item d-flex justify-content-between align-items-center">
            <router-link :to="'/songinfo/' + song.id " class="btn btn-primary" >{{ song.name }}</router-link>
            <div>
              <button @click="playSong(song.path)" class="btn btn-primary btn-sm">Play</button>
              <button @click="removeFromPlaylist(song.id)" class="btn btn-danger btn-sm ml-2">Remove</button>
            </div>
          </li>
        </ul>
      </div>
      <audio id="audioPlayer" controls :src="'http://127.0.0.1:5000/' + currentSongPath" v-if="isPlaying" class="mt-4"></audio>
    </div>
</template>
  
  
<script>
  export default {
    data() {
      return {
        playlists: [], 
        newPlaylistName: '', 
        currentPlaylist: [], 

        showPlaylisttoggle:false,
        currentPlaylistName:'',
        currentPlaylistId:0,

        currentSongPath: '',
        isPlaying: false,

        user_id: parseInt(localStorage.user_id)
      };
    },
    mounted(){
      this.checkUser();
        this.fetchplaylists()
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
      createPlaylist() {
        try{
            fetch(`http://127.0.0.1:5000/playlists/${this.user_id}`,{
              method:'POST',
              body:JSON.stringify({'playlist_id':'new','new_playlist_name':this.newPlaylistName,'song_ids':[]}),
              headers:{
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.token}`
              }
            })
            .then(response => {
                return response.json();
            })
            .then(data => {
                console.log(data)
                this.fetchplaylists()
            })
        }catch{

        }
      },
      deletePlaylist(id){
        try{
            fetch(`http://127.0.0.1:5000/playlists/${parseInt(id)}`,{
                method:'DELETE',
                headers:{
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${localStorage.token}`
                }
            })
            .then(response => {
                return response.json();
            })
            .then(data => {
                console.log(data)
                this.fetchplaylists()
            })
        }catch{

        }
      },
      showPlaylist(playlistId,playlistName) {
        // Fetch playlist songs based on playlistId and update this.currentPlaylist
        try{
            fetch(`http://127.0.0.1:5000/showpl/${parseInt(playlistId)}`,{
              method: 'GET',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.token}`
              }
            })
            .then(response => {
                return response.json();
            })
            .then(data => {
                console.log(data)
                this.showPlaylisttoggle=true
                this.currentPlaylist=data
                this.currentPlaylistName=playlistName
                this.currentPlaylistId=playlistId
            })
        }catch{

        }
      },
      playSong(songPath) {
        this.currentSongPath = songPath;
        this.isPlaying = true;
      },
      removeFromPlaylist(songId) {
        fetch(`http://127.0.0.1:5000/removesongfrompl/${parseInt(this.currentPlaylistId)}/${parseInt(songId)}`,{
            headers:{
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            this.isPlaying = false;
            alert("song removed from playlist")
            this.showPlaylist(this.currentPlaylistId,this.currentPlaylistName)
        })
      },

      fetchplaylists(){
        fetch(`http://127.0.0.1:5000/playlists/${this.user_id}/${0}`,{
            method:'GET',
            headers:{
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            this.playlists=data
        })
        .catch(error => {
            console.log(error)
        })
      }
    },
  };
</script>
  
<style scoped>

</style>
  