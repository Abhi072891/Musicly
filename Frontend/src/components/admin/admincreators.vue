<template>
    <div v-for="creator in creators" :key="creator.user_id" class="creator-item">
        <button @click="showSongsAndAlbums(creator.user_id)">{{ creator.username }}</button>
        <p>Status: {{ creator.status }}</p>
        <span v-if="creator.status === 'blc'" class="status-icon red-circle">&#10006;</span>
        <span v-else-if="creator.status === 'wlc'" class="status-icon green-circle">&#10004;</span>
        <button @click="whitelistCreator(creator.user_id)" v-if="creator.status === 'blc'">Whitelist</button>
        <button @click="blacklistCreator(creator.user_id)" v-if="creator.status === 'wlc'">Blacklist</button>
        <div v-if="selectedCreatorId === true">
            <div v-if="songs.length > 0">
                <div v-for="song in songs" :key="song.song_id" class="song-item">
                    <p>{{ song.song_name }}</p>
                    <button @click="deleteSong(song.song_id)">Delete</button>
                </div>
                <div v-for="album in albums" :key="album.album_id" class="album-item">
                    <p>{{ album.album_name }}</p>
                    <button @click="deleteAlbum(album.album_id)">Delete</button>
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
      this.fetchCreators();
    },
    methods: {
        fetchCreators() {
            fetch('http://127.0.0.1:5000/allcreators')
                .then(response => response.json())
                .then(data => {
                this.creators = data;
                })
                .catch(error => {
                console.error('Error fetching creators:', error);
            });
        },
        whitelistCreator(userId) {
            fetch(`http://127.0.0.1:5000/whitelistcreator/${parseInt(userId)}`)
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
            fetch(`http://127.0.0.1:5000/blacklistcreator/${parseInt(userId)}`)
                .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                console.log('Creator blacklisted successfully');
                this.fetchCreators(); // Refresh the list of creators
                })
                .catch(error => {
                console.error('Error blacklisting creator:', error);
            });
        },
        showSongsAndAlbums(creatorId) {
            creatorId=parseInt(creatorId)
            this.selectedCreatorId=true
            fetch(`http://127.0.0.1:5000/albumsbyuser/${creatorId}`)
                .then(respose => respose.json())
                .then(data => {
                    this.albums=data
                })
                .catch(error => console.log(error))
                
            fetch(`http://127.0.0.1:5000/songsbyuser/${creatorId}`)
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
  
<style>
/* Add your CSS styles here */
</style>
  