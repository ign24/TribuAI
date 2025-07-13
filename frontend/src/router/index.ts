import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { title: 'TribuAI - Discover Your Cultural Identity' }
    }
  ]
});

router.beforeEach((to) => {
  document.title = to.meta.title as string || 'TribuAI';
});

export default router;