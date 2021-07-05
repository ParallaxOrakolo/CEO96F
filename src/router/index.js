import Vue from 'vue'
import Router from 'vue-router'


import Home from '@/views/Home'
import Settings from '@/views/Settings'
import Intro from '@/views/Intro'
import Scan from '@/views/Scan'
import Progress from '@/views/Progress'

Vue.use(Router)

const routes = [
    {
        name: 'home',
        path:'/home',
        component: Home,
    },
    {
        name: 'settings',
        path:'/config',
        component: Settings,
    },
    {
        name: 'intro',
        path:'/',
        component: Intro,
    },
     {
        name: 'scan',
        path:'/scan',
        component: Scan,
    },
    {
        name: 'progress',
        path:'/progress',
        component: Progress,
    },
]

const router = new Router({ routes})

export default router