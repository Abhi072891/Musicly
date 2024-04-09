<section>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <router-link class="navbar-brand" to="/">Your Logo</router-link>
            
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item">
                        <router-link class="nav-link" to="/home0">Home</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/songs/0">Songs</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/albums/0">Albums</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/artists/0">Artists</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/allplaylist/{{user_id}}">Playlists</router-link>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</section>

<style scoped>
        /* Custom CSS for Navbar */
        .navbar {
            background-color: #343a40;
        }

        .navbar-dark .navbar-nav .nav-link {
            color: #ffffff; 
        }

        .navbar-dark .navbar-toggler-icon {
            background-color: #ffffff; 
        }

        .navbar-dark .navbar-toggler {
            border-color: #ffffff;
        }

        .navbar-nav .nav-item {
            margin-right: 20px; 
        }

        .navbar-nav .nav-link {
            font-weight: bold;
        }
        
      
</style>


<script>
export default {
    name: 'navbar',
    // props: ['user_id'] 
}
</script>
