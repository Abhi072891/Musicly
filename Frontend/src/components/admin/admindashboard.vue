<template>
    <div class="admin-dashboard">
      <h2>Admin Dashboard</h2>
      <div class="statistics">
        <div class="box" >
          <h3>Total Users: {{ totalUsers }}</h3>
        </div>
        <div class="box" @click="navigateToCreatorsPage">
          <h3>Total Creators: {{ totalCreators }}</h3>
        </div>
        <div class="box" @click="navigateToSongsPage">
          <h3>Total Songs: {{ totalSongs }}</h3>
        </div>
        <div class="box" @click="navigateToAlbumsPage">
          <h3>Total Albums: {{ totalAlbums }}</h3>
        </div>
      </div>
      <div class="creator-applications">
        <button @click="navigateToCreatorApplications">Creator Applications</button>
      </div>
      <button @click="Chart" class="btn btn-warning">Plot charts</button>
    </div>
    <canvas id="songChart" ></canvas>
    <canvas id="albumChart" ></canvas>
</template>

<script>
  export default {
    data() {
      return {
        totalUsers: 0,
        totalCreators: 0,
        totalSongs: 0,
        totalAlbums: 0,
        songs:[],
        albums:[],

      };
    },
    mounted() {
      this.checkUser();
      this.fetchStatistics();
    },
    methods: {
      checkUser(){
        if (!localStorage.token) {
          alert("Login again")
          this.$router.push('/adminlogin');
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
          this.$router.push('/adminlogin');
        });

        if(localStorage.user_role!="admin"){
            alert('not a admin')
            this.$router.push('/home')
        }
      },
      fetchStatistics() {
        fetch(`http://127.0.0.1:5000/adminstats`,{
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.token}`
          }
        })
        .then(respose => respose.json())
        .then(data => {
            this.totalUsers = data.user_count
            this.totalCreators = data.creator_count
            this.totalSongs = data.song_count
            this.totalAlbums = data.album_count
        })
        .catch(error => console.log(error))
      },
      navigateToCreatorsPage() {
        this.$router.push('/admincreators');
      },
      navigateToSongsPage() {
        this.$router.push('/adminsongs');
      },
      navigateToAlbumsPage() {
        this.$router.push('/adminalbums');
      },
      navigateToCreatorApplications() {
        this.$router.push('/waiting-creator-application');
      },

      Chart(){
        fetch('http://127.0.0.1:5000/songs/0', {
          method:"GET",
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
          this.songs = [...data].sort((a, b) => b.pcount - a.pcount);
          if(this.songs.length>5){
            const songLabels = this.songs.slice(0, 5).map(song => song.song_name);
            const songValues = this.songs.slice(0, 5).map(song => song.pcount);
            this.createChart('songChart', songLabels, songValues);
          } else{
            const songLabels = this.songs.map(song => song.song_name);
            const songValues = this.songs.map(song => song.pcount);
            this.createChart('songChart', songLabels, songValues);
          }
        })

        fetch(`http://127.0.0.1:5000/albums/0`,{
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.token}`
          }
          })
          .then(response => response.json())
          .then(data => {
            this.albums = [...data].sort((a, b) => b.rcount - a.rcount);
            if(this.albums.length>6){
              const albumLabels = data.slice(0, 5).map(album => album.album_name);
              const albumValues = data.slice(0, 5).map(album => album.rcount);
              this.createChart('albumChart', albumLabels, albumValues);
            }else{
              const albumLabels = data.map(album => album.album_name);
              const albumValues = data.map(album => album.rcount);
              this.createChart('albumChart', albumLabels, albumValues);
            }
          })
      },
      createChart(canvasId, labels, values) {
          const ctx = document.getElementById(canvasId).getContext('2d');
          new Chart(ctx, {
              type: 'bar',
              data: {
                  labels: labels,
                  datasets: [{
                      label: 'Count',
                      data: values,
                      backgroundColor: [
                          'rgba(255, 99, 132, 0.2)', // Red
                          'rgba(54, 162, 235, 0.2)', // Blue
                          'rgba(255, 206, 86, 0.2)', // Yellow
                          'rgba(75, 192, 192, 0.2)', // Green
                          'rgba(153, 102, 255, 0.2)' // Purple
                      ],
                      borderColor: [
                          'rgba(255, 99, 132, 1)', // Red
                          'rgba(54, 162, 235, 1)', // Blue
                          'rgba(255, 206, 86, 1)', // Yellow
                          'rgba(75, 192, 192, 1)', // Green
                          'rgba(153, 102, 255, 1)' // Purple
                      ],
                      borderWidth: 1
                  }]
              },
              options: {
                  scales: {
                      yAxes: [{
                          ticks: {
                              beginAtZero: true
                          }
                      }]
                  },
                  // responsive: true,
                  // maintainAspectRatio: false
              }
          });
        }

      }
    
  };
</script>

<style scoped>
  .admin-dashboard {
    padding: 20px;
  }
  .statistics {
    display: flex;
    flex-wrap: wrap;
  }
  .box {
    width: 200px;
    height: 150px;
    background-color: #f0f0f0;
    margin: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
  }
  .creator-applications button {
    background-color: #007bff;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
</style>
  