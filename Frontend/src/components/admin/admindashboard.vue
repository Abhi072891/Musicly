<template>
    <div class="admin-dashboard">
      <h2>Admin Dashboard</h2>
      <div class="statistics">
        <!-- <div class="box" @click="navigateToUsersPage"> -->
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
    </div>
</template>

<script>
  export default {
    data() {
      return {
        totalUsers: 0,
        totalCreators: 0,
        totalSongs: 0,
        totalAlbums: 0
      };
    },
    mounted() {
      this.fetchStatistics();
    },
    methods: {
      fetchStatistics() {
        // Implement fetch requests to get statistics data
        // Assign fetched data to the corresponding data properties
        fetch(`http://127.0.0.1:5000/adminstats`)
        .then(respose => respose.json())
        .then(data => {
            this.totalUsers = data.user_count
            this.totalCreators = data.creator_count
            this.totalSongs = data.song_count
            this.totalAlbums = data.album_count
        })
        .catch(error => console.log(error))
      },
    //   navigateToUsersPage() {
    //     this.$router.push('/users');
    //   },
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
  