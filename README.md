# Musicly 

🎧 Musicly is a basic music streaming platform designed for ease of use, featuring dual access for both users and creators. It provides a robust set of features for managing playlists, Albums, Artists, track performances.

## Author
- **Name:** Abhishek Singh
- **Roll Number:** 22f3001196
- **Email:** 22f3001196@ds.study.iitm.ac.in

## About
I am a full-time student of IITM BS, currently in the diploma level of programming.

## Project Description
Larder Vault is a comprehensive music streaming platform built with Vue.js for the front end and Python-Flask for the back end. It allows users to play songs, make playlists, and offers enhanced control for administrators and creators. The platform also provides graphical insights into performance data for popularity analysis of songs and albums.

## Demo Video
[Watch Demo Video Here](https://drive.google.com/file/d/1WnN01rToYgdB5OUPCjz8e7CcOZs8TzTF/view?usp=drive_link)

## Technologies Used
- **Python**: Primary language for controller development and hosting the app.
- **Vue.js**: Front-end development.
- **HTML**: Creation of Vue components and templates.
- **Bootstrap**: Enhancing front-end design and navigation.
- **SQLite**: Database for the app.
- **Flask**: Web framework of the app.
- **Flask-SQLAlchemy**: Accessing and modifying SQLite database.
- **Flask-Celery**: Handling asynchronous background jobs.
- **Flask-Caching**: Caching API outputs for improved performance.
- **Redis**: In-memory database for API cache and message broker for Celery.
- **Chart.js**: Generating various charts.
- **Git**: Version control management.

## Architecture and Features
Musicly follows a client-server model with Vue.js for the front end and Python-Flask for the back end. It incorporates various features to provide a seamless music streaming experience:

### Dual Access with Enhanced Admin Control
- **Distinct Access Points:** Separate access for users, creators and adminstrator.
- **Creator Signup:** Streamlined signup process for creators.
- **Approval System:** Admin approval required for creator registration application and admin can also retrieve creator privilge.

### User Features
-**Streaming:** Users can play songs and can see lyrics and can also access related albums and artists of song.
- **Convenient Playlist managment:** Users can add, edit, or remove songs form playlists.
- **Rating:** Users can rate a song.

### Song and Album Management
- **Control:** Administrators and creator can manage and delete existing song and albums.

### Graphical Performance Analytics
- **Insights:** Utilizing Chart.js to provide graphical insights into popularity data for songs and albums.

### User Authentication
- **Secure Access:** Robust mechanisms for user signup and login.

### Database Integration
- **SQLite:** Used for database needs.
- **Flask-SQLAlchemy:** Effective data handling.

### Asynchronous Task Handling
- **Flask-Celery:** Managing background tasks for optimized efficiency.

### API Caching for Performance
- **Flask-Caching and Redis:** Caching API outputs and in-memory database for improved performance.

### Comprehensive RESTful API
- **Well-Structured:** API for interacting with product data, user accounts, and other essential elements.

### Responsive and Attractive UI
- **Bootstrap and Vue.js:** Delivering a user-friendly and aesthetically pleasing interface.


## Installation
To install and run Musicly, follow these steps:

1. **Clone Repository:**
   ```bash
   git clone https://github.com/username/repository.git

2. **Install Dependencies:**
   ```bash
   cd <repository_directory>
   pip install -r requirements.txt
   npm install

3. **Run Application:**
   ```bash
   flask run

The application should now be running locally.

**Access Application:**
Open your web browser and go to [http://localhost:5000](http://localhost:5000) to access the Larder Vault application.
