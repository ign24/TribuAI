import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import ResultsView from '@/views/ResultsView.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { title: 'TribuAI - Discover Your Cultural Identity' }
    },
    {
      path: '/results',
      name: 'results',
      component: ResultsView,
      meta: { title: 'Your Cultural Profile - TribuAI' }
    }
  ]
});

router.beforeEach((to) => {
  document.title = to.meta.title as string || 'TribuAI';
});

export default router;