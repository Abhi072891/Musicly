import { createRouter, createWebHistory } from 'vue-router'

import home from '../components/home.vue'

import songs from '../components/songs.vue';
import songinfo from '@/components/songinfo.vue';
import genre from '@/components/genre.vue';

import login from '../components/login.vue';
import register from "../components/register.vue";

import albums from '@/components/albums.vue';
import albuminfo from '@/components/albuminfo.vue';

import artists from '@/components/artists.vue';
import artistinfo from '@/components/artistinfo.vue';

import playlist from '@/components/playlist.vue';

import creatordashboard from '@/components/creator/creatordashboard.vue'
import creatorapplication from '@/components/creator/creator-application.vue'
import songupload from '@/components/creator/songupload.vue';
import createalbum from '@/components/creator/createalbum.vue'
import editalbum from '@/components/creator/editalbum.vue'
import editsong from '@/components/creator/editsong.vue'

import adminlogin from '@/components/admin/adminlogin.vue'
import admindashboard from '@/components/admin/admindashboard.vue'
import adminsongs from '@/components/admin/adminsongs.vue'
import adminalbums from '@/components/admin/adminalbums.vue'
import admincreators from '@/components/admin/admincreators.vue'
import waitingcreatorapplication from '@/components/admin/waitingcreatorsapplication.vue'

const routes = [

  {
    path: '/login',
    name: 'login',
    component: login
  },
  {
    path: '/register',
    name: 'register',
    component: register
  },

  {
    path: '/home',
    name: 'home',
    component: home
  },

  {
    path:'/songs',
    name:'songs',
    component: songs
  },
  {
    path: '/songinfo/:songId',
    name: 'songinfo',
    component: songinfo,
    props: true,
  },
  {
    path: '/genre/:genre',
    name: 'genre',
    component: genre,
    props: true,
  },


  {
    path:'/albums',
    name:'albums',
    component: albums
  },
  {
    path:'/albums/:albumId',
    name:'albuminfo',
    component: albuminfo
  },


  {
    path:'/artists',
    name:'artists',
    component: artists
  },
  {
    path:'/artists/:artistId',
    name:'artistinfo',
    component: artistinfo
  },
  

  {
    path:'/playlist',
    name: 'playlist',
    component: playlist
  },
                // ###############Creator###########
  {
    path: '/creator',
    name: 'creatordashboard',
    component: creatordashboard
  },
  {
    path: '/songupload',
    name: 'songupload',
    component: songupload,
  },
  {
    path: '/creator-application',
    name: 'creator-application',
    component: creatorapplication
  },
  {
    path: '/createalbum',
    name: 'createalbum',
    component: createalbum
  },
  {
    path: '/editalbum/:albumId',
    name: 'editalbum',
    component: editalbum,
    props: true,
  },
  {
    path: '/editsong/:songId',
    name: 'editsong',
    component: editsong,
    props: true,
  },

            //#################Admin##############
  {
    path: '/adminlogin',
    name: 'adminlogin',
    component: adminlogin,
  },
  {
    path: '/admindashboard',
    name: 'admindashboard',
    component: admindashboard
  },
  {
    path: '/adminsongs',
    name: 'adminsongs',
    component: adminsongs
  },
  {
    path: '/adminalbums',
    name: 'adminalbums',
    component: adminalbums
  },
  {
    path: '/admincreators',
    name: 'admincreators',
    component: admincreators
  },
  {
    path: '/waiting-creator-application',
    name: 'waiting-creator-application',
    component: waitingcreatorapplication
  },


]

const router = createRouter({
  history: createWebHistory(),
  routes
})


export default router



