<template>
  <div class="container">
    <router-link to="/creator" class="btn btn-secondary">Go back</router-link>
    <h1 style="color: #0056b3;">Upload a Song</h1>
    <form @submit.prevent="submitForm" enctype="multipart/form-data">
      <div class="form-group">
        <label for="songname" class="required">Name of the Song:</label>
        <input type="text" v-model="formData.songname" required class="form-control">
      </div>
      <div class="form-group">
        <label for="artistname">Name of Artists (Comma Separated):</label>
        <input type="text" v-model="formData.artistname" placeholder="Artist1, Artist2" class="form-control">
      </div>
      <div class="form-group">
      <label for="genre">Genres:</label>
      <select v-model="formData.genre" class="form-control">
        <option value="none">None</option>
        <option v-for="genre in genres" :key="genre" :value="genre">{{ genre }}</option>
      </select>
    </div>
      <div class="form-group">
        <label for="album">Album:</label>
        <select v-model="formData.album" class="form-control" @change="toggleAlbumInput()">
          <option value="none">None</option>
          <option value="new">Create a New Album</option>
          <option v-for="album in albums" :value="album.album_name">{{ album.album_name }}</option>
        </select>
        <input type="text" v-if="formData.album === 'new'" v-model="formData.new_album_name"
          placeholder="Give Name for Album" class="form-control">
      </div>
      <div class="form-group">
        <label for="lyrics">Lyrics for the Song:</label>
        <textarea v-model="formData.lyrics" rows="5" cols="40" class="form-control"></textarea>
      </div>
      <div class="form-group file-input">
        <label for="songfile" class="required">Select Song (MP3 only):</label>
        <input type="file" @change="handleFileChange" accept=".mp3" class="form-control">
      </div>
      <div class="form-group">
        <input type="submit" value="Upload" class="btn btn-primary">
      </div>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      formData: {
        songname: '',
        artistname: '',
        genre: 'none',
        album: 'none',
        new_album_name: '',
        lyrics: '',
        songfile: null
      },
      genres: ['Pop', 'Rock', 'Hip-Hop', 'Jazz', 'Country', 'Electronic', 'R&B', 'Reggae', 'Classical', 'Blues', 'Metal', 'Alternative', 'Indie', 'Folk', 'Punk', 'Other'],
      user_id: parseInt(localStorage.user_id),
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

        if(localStorage.user_role==='user'){
            alert("not a creator")
            this.$router.push('/home')
        }
    },
    toggleAlbumInput() {
      // Logic for toggling album input
    },
    handleFileChange(event) {
      this.formData.songfile = event.target.files[0];
    },
    fetchAlbums() {
      fetch(`http://127.0.0.1:5000/albums/0`,{
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.token}`
          }
        })
        .then(response => response.json())
        .then(data => {
          this.albums = data; 
        })
        .catch(error => {
          console.error('Error fetching albums data:', error);
        });
    },
    submitForm() {
      let formData = new FormData();
      for (let key in this.formData) {
        formData.append(key, this.formData[key]);
      }
      console.log(formData)
      fetch(`http://127.0.0.1:5000/songs/${this.user_id}`, {
          method: 'POST',
          body: formData,
          headers: {
            'Authorization': `Bearer ${localStorage.token}`
          }
        })
        .then(response => {
          if (response.ok) {
            return response.json()
          } else {
            throw new Error('Failed to upload song');
          }
        })
        .then(data => {
          alert('Song uploaded successfully')
          this.$router.push('/creator')
        })
        .catch(error => {
          alert('couldnot upload the song')
          // window.location.reload()
        });
    }
  }
};
</script>


<style scoped>
body {
  font-family: 'Arial', sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f2f2f2;
}

.container {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  padding: 20px;
  max-width: 600px;
  margin: 20px auto;
}

label.required::before {
  content: "*";
  color: red;
}

select.form-control,
input.form-control,
textarea.form-control {
  width: 96%;
  padding: 12px;
  margin: 8px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f8f8f8;
  font-size: 16px;
}

.btn-primary {
  background-color: #007BFF;
  color: #fff;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.form-group {
  text-align: left;
  margin: 20px 0;
}

.file-input {
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 2px dashed #007BFF;
  padding: 20px;
  background-color: #f8f8f8;
  border-radius: 5px;
}
</style>
