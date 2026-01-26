import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomePage.vue'),
    },
    {
      path: '/worksheets',
      name: 'worksheets',
      component: () => import('@/views/WorksheetListPage.vue'),
    },
    {
      path: '/category/:slug',
      name: 'category',
      component: () => import('@/views/WorksheetListPage.vue'),
      props: true,
    },
    {
      path: '/worksheet/:slug',
      name: 'worksheet-detail',
      component: () => import('@/views/WorksheetDetailPage.vue'),
      props: true,
    },
    {
      path: '/tag/:slug',
      name: 'tag',
      component: () => import('@/views/WorksheetListPage.vue'),
      props: true,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('@/views/StaticPage.vue'),
      props: { slug: 'about' },
    },
    {
      path: '/contacts',
      name: 'contacts',
      component: () => import('@/views/StaticPage.vue'),
      props: { slug: 'contacts' },
    },
    {
      path: '/terms',
      name: 'terms',
      component: () => import('@/views/StaticPage.vue'),
      props: { slug: 'terms' },
    },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
