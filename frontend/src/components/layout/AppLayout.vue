<template>
  <div class="min-h-screen bg-obsidian">
    <!-- Animated Background -->
    <vue-particles
      id="tsparticles"
      :options="particlesOptions"
      class="fixed inset-0 z-0"
    />
    
    <!-- Main Content -->
    <div class="relative z-10 min-h-screen">
      <AppHeader v-if="showHeader" />
      <main class="flex-1">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import AppHeader from './AppHeader.vue';

interface Props {
  showHeader?: boolean;
}

withDefaults(defineProps<Props>(), {
  showHeader: true
});

const particlesOptions = computed(() => ({
  fpsLimit: 120,
  interactivity: {
    events: {
      onClick: {
        enable: false,
        mode: "push",
      },
      onHover: {
        enable: true,
        mode: "grab",
      },
      resize: {
        enable: true,
        delay: 0.5
      },
    },
    modes: {
      push: {
        quantity: 4,
      },
      grab: {
        distance: 100,
        links: {
          opacity: 0.1
        }
      },
    },
  },
  particles: {
    color: {
      value: ["#00F5FF", "#8338EC", "#FF006E"],
    },
    links: {
      color: "#00F5FF",
      distance: 150,
      enable: true,
      opacity: 0.15,
      width: 1,
    },
    move: {
      enable: true,
      speed: 0.5,
      direction: "none",
      random: false,
      straight: false,
      outModes: {
        default: "bounce",
      },
    },
    number: {
      density: {
        enable: true,
        value_area: 800,
      },
      value: 60,
    },
    opacity: {
      value: 0.15,
      animation: {
        enable: true,
        speed: 0.5,
        opacity_min: 0.05,
        sync: false,
      },
    },
    shape: {
      type: "circle",
    },
    size: {
      value: 2,
      random: true,
      animation: {
        enable: true,
        speed: 1,
        size_min: 0.1,
        sync: false,
      },
    },
  },
  detectRetina: true,
}));
</script>