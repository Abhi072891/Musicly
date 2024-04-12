<template>
    <div v-if="songs.length > 0">
        <h2>Songs :</h2>
        <ul class="list-group">
            <li v-for="song in songs" :key="song.song_id" class="list-group-item">
                <div class="d-flex justify-content-between align-items-center">
                <span>{{ song.song_name }}</span>
                <div class="btn-group">
                    <button @click="deleteSong(song.song_id)" class="btn btn-danger">Delete</button>
                    <router-link :to="'/songinfo/' + song.song_id" class="btn btn-primary">Go to Song</router-link>
                </div>
                </div>
            </li>
        </ul>
      </div>
</template>

<script>
    export default {
    data() {
      return {
        songs: [],
      };
    },
    mounted() {
      this.checkUserRole();
      this.fetchSongs();
    },
    methods: {
      checkUserRole() {
      const role = localStorage.getItem('user_role');
      if (role != 'admin') {
        alert("Your are not a Admin!!")
        this.$router.push('/home');
      }
    },
      fetchSongs() {
        fetch(`http://127.0.0.1:5000/songs/0`)
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
    }
  };
</script>

<style scoped>

</style>