import Vue from 'vue'
import Router from 'vue-router'

import Home from '@/views/Home'
import Settings from '@/views/Settings'
import IntroLogo from '@/views/IntroLogo'
import Success from '@/views/Success'
import Scan from '@/views/Scan'
import Progress from '@/views/Progress'
import Dashboard from '@/views/Dashboard'

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
        name: 'intro-logo',
        path:'/',
        component: IntroLogo,
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
    {
        name: 'success',
        path:'/success',
        component: Success,
    },
    {
        name: 'dashboard',
        path:'/dashboard',
        component: Dashboard,
    },
]

const router = new Router({ routes})

export default router