<template>
    <div>
      <div v-for="creator in creators" :key="creator.user_id" class="creator-item card mb-3">
        <div class="card-body">
          <button @click="showSongsAndAlbums(creator.user_id)" class="btn btn-link">{{ creator.username }}</button>
          <p>Status: {{ creator.status }}</p>
          <span v-if="creator.status === 'blc'" class="status-icon red-circle">❌</span>
          <span v-else-if="creator.status === 'wlc'" class="status-icon green-circle">✅</span>
          <button @click="whitelistCreator(creator.user_id)" v-if="creator.status === 'blc'" class="btn btn-success">Whitelist</button>
          <button @click="blacklistCreator(creator.user_id)" v-if="creator.status === 'wlc'" class="btn btn-danger">Blacklist</button>
          <div v-if="selectedCreatorId === creator.user_id" class="mt-3">
            <div v-if="songs.length > 0">
              <h5>Songs</h5>
              <div v-for="song in songs" :key="song.song_id" class="song-item">
                <p>{{ song.song_name }}</p>
                <button @click="deleteSong(song.song_id)" class="btn btn-danger">Delete</button>
              </div>
            </div>
            <div v-if="albums.length > 0">
              <h5>Albums</h5>
              <div v-for="album in albums" :key="album.album_id" class="album-item">
                <p>{{ album.album_name }}</p>
                <button @click="deleteAlbum(album.album_id)" class="btn btn-danger">Delete</button>
              </div>
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
        creators: [],
        selectedCreatorId: false,
        songs:[],
        albums:[]
      };
    },
    mounted() {
      this.checkUser();
      this.fetchCreators();
    },
    methods: {
      checkUser(){
        if (!localStorage.token) {
          alert("Login again")
          this.$router.push('/login');
        }
        fetch('http://127.0.0.1:5000/jwt/testing', {
          headers: {
            method: 'GET',
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

        if(localStorage.user_role!="admin"){
            alert('not a admin')
            window.location.reload()
        }
      },
      fetchCreators() {
        fetch('http://127.0.0.1:5000/allcreators',{
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.token}`
            }
          })
          .then(response => response.json())
          .then(data => {
          this.creators = data;
          })
          .catch(error => {
          console.error('Error fetching creators:', error);
          });
      },
      whitelistCreator(userId) {
          fetch(`http://127.0.0.1:5000/whitelistcreator/${parseInt(userId)}`,{
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
            console.log('Creator whitelisted successfully');
            this.fetchCreators(); // Refresh the list of creators
            })
            .catch(error => {
            console.error('Error whitelisting creator:', error);
            });
      },
      blacklistCreator(userId) {
          fetch(`http://127.0.0.1:5000/blacklistcreator/${parseInt(userId)}`,{
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
            console.log('Creator blacklisted successfully');
            this.fetchCreators(); 
            })
            .catch(error => {
            console.error('Error blacklisting creator:', error);
            });
      },
      showSongsAndAlbums(creatorId) {
        creatorId=parseInt(creatorId)
        this.selectedCreatorId=true
        fetch(`http://127.0.0.1:5000/albumsbyuser/${creatorId}`,{
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.token}`
            }
          })
          .then(respose => respose.json())
          .then(data => {
              this.albums=data
          })
          .catch(error => console.log(error))
            
        fetch(`http://127.0.0.1:5000/songsbyuser/${creatorId}`,{
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.token}`
            }
          })
          .then(respose => respose.json())
          .then(data => {
              this.songs=data
          })
          .catch(error => console.log(error))
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
                  window.location.reload()
                })
              .catch(error => {
                console.error('Error deleting song:', error);
                window.location.reload()
              });
          }
      },
      deleteAlbum(albumId) {
        if (confirm("Are you sure you want to delete this album?")) {
          fetch(`http://127.0.0.1:5000/albums/${parseInt(albumId)}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.token}` 
            }
          })
          .then(response => {
            if (response.ok) {
                alert("Album deleted successfully");
                window.location.reload()
            } else {
                alert("Failed to delete album");
                window.location.reload()
            }
          })
          .catch(error => {
              console.error('Error deleting album:', error);
              alert("Failed to delete album");
              window.location.reload()
          });
        }
      }
    }
  };
</script>
  
<style scoped>
.creator-item {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
}

.status-icon {
  font-size: 24px;
  margin-left: 10px;
}

.red-circle {
  color: red;
}

.green-circle {
  color: green;
}

.song-item, .album-item {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  margin-top: 10px;
}

.btn {
  margin-right: 5px;
}
</style>
  