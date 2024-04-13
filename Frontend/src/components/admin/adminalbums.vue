<template>
    <div v-if="albums.length > 0">
        <h2>Albums : </h2>
        <ul class="list-group">
            <li v-for="album in albums" :key="album.album_id" class="list-group-item">
                <div class="d-flex justify-content-between align-items-center">
                    <span>{{ album.album_name }}</span>
                    <div class="btn-group ml-2">
                        <button @click="deleteAlbum(album.album_id)" class="btn btn-danger">Delete</button>
                        <router-link :to="'/albums/' + album.album_id" class="btn btn-primary">Go to Album</router-link>
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
        albums: [],
      };
    },
    mounted() {
      this.checkUser();
      this.fetchAlbums();
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
        fetchAlbums() {
            fetch(`http://127.0.0.1:5000/albums/0`,{
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

</style>