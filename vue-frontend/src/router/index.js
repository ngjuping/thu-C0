import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '@/views/Login.vue'
import store from '../store';

Vue.use(VueRouter);

const routes = [
  { 
    path: '/', 
    redirect: { name: 'Login' }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/signup',
    name: 'Signup',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '@/views/Signup.vue')
  },
  {
    path: '/main',
    name: 'Mainpage',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '@/views/Mainpage.vue')
  },
  {
    path:'/admin',
    name:'Admin',
    redirect: '/admin/venues',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '@/views/Admin.vue'),
    children: [
      {
        path:'/admin/venues',
        name:'Venues',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '@/views/Venues.vue')
      },
      {
        path:'/admin/replyFeedback',
        name:'ReplyFeedback',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '@/views/ReplyFeedback.vue')
      },
      {
        path:'/admin/noticeManager',
        name:'NoticeManager',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '@/views/NoticeManager.vue')
      },
      {
        path:'/admin/trainManager',
        name:'TrainManager',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '@/views/TrainManager.vue')
      },
      {
        path:'/admin/fieldInit',
        name:'FieldInit',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '@/views/FieldInit.vue')
      },
    ]
  },
  {
    path: '/booking/:venueid',
    name: 'Booking',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '@/views/Booking.vue')
  },
  {
    path: '/manage',
    name: 'Manage',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '@/views/Manage.vue')
  },
  {
    path: '/notices',
    name: 'AllNotices',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '@/views/AllNotices.vue')
  },
  {
    path: '/feedbacks',
    name: 'AllFeedbacks',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '@/views/AllFeedbacks.vue')
  },
  {
    path: '/shares',
    name: 'AllShares',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '@/views/AllShares.vue')
  },
  {
    path: '/courses',
    name: 'AllCourses',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '@/views/AllCourses.vue')
  },
  {
    path: '*',
    name: '404page',
    component: () => import(/* webpackChunkName: "about" */ '@/views/NotFound.vue')
  }
]

const router = new VueRouter({
  routes
})

router.beforeEach((to, from, next) => {
  let user_pages = ["AllCourses","AllShares","AllFeedbacks","AllNotices","Manage","Booking","Mainpage"];
  let admin_pages = ["Admin","Venues","ReplyFeedback","NoticeManager","TrainManager","FieldInit"];
  let accessingUserPage = Boolean(user_pages.indexOf(to.name) != -1);
  let accessingAdminPage = Boolean(admin_pages.indexOf(to.name) != -1);
  let isAdmin = Boolean(store.state.privilege === 1);
  let isUser = Boolean(!store.state.privilege);
  let noPrivilege = Boolean(store.state.privilege === -1);
  if(accessingUserPage && isAdmin){
    next(false);
  }
  else if(accessingAdminPage && isUser){
    next(false);
  }
  else if(noPrivilege && accessingAdminPage){
    next(false);
  }
  else{
    next();
  }
})

export default router
