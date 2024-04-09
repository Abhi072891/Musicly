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
import songupload from '@/components/creator/songupload.vue';
import createalbum from '@/components/creator/createalbum.vue'
import editalbum from '@/components/creator/editalbum.vue'
import editsong from '@/components/creator/editsong.vue'

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
  
  {
    path: '/songupload',
    name: 'songupload',
    component: songupload,
  },
  {
    path: '/creator',
    name: 'creatordashboard',
    component: creatordashboard
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



]

const router = createRouter({
  history: createWebHistory(),
  routes
})


export default router



