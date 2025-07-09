<template>
  <svg
    :class="iconClasses"
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <!-- Profile Icon -->
    <path
      v-if="name === 'profile'"
      d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L12 2L3 7V9H21ZM12 13.5C12 14.3 11.3 15 10.5 15C9.7 15 9 14.3 9 13.5C9 12.7 9.7 12 10.5 12C11.3 12 12 12.7 12 13.5ZM12 22C14.7 22 17 19.7 17 17V15H7V17C7 19.7 9.3 22 12 22Z"
      :fill="currentColor"
    />
    
    <!-- Brands Icon -->
    <path
      v-if="name === 'brands'"
      d="M12 2L2 7V10C2 16 6 20.9 12 22C18 20.9 22 16 22 10V7L12 2ZM12 4.3L20 8.2V10C20 15.1 16.7 19.1 12 20C7.3 19.1 4 15.1 4 10V8.2L12 4.3Z"
      :fill="currentColor"
    />
    
    <!-- Globe Icon -->
    <path
      v-if="name === 'globe'"
      d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM4 12C4 7.59 7.59 4 12 4C13.79 4 15.42 4.56 16.75 5.5C15.5 6.5 14.5 8 14.5 10C14.5 12 16 13.5 18 13.5C18.34 13.5 18.67 13.43 19 13.3C19 16.97 16.97 19 13.3 19C12.43 19 11.67 18.66 11.12 18.12L10 17C9 16 8 15.5 7 15.5C5.5 15.5 4 16.5 4 18V12Z"
      :fill="currentColor"
    />
    
    <!-- Match Icon -->
    <path
      v-if="name === 'match'"
      d="M12 21.35L10.55 20.03C5.4 15.36 2 12.27 2 8.5C2 5.41 4.42 3 7.5 3C9.24 3 10.91 3.81 12 5.08C13.09 3.81 14.76 3 16.5 3C19.58 3 22 5.41 22 8.5C22 12.27 18.6 15.36 13.45 20.03L12 21.35Z"
      :fill="currentColor"
    />
    
    <!-- Summary Icon -->
    <path
      v-if="name === 'summary'"
      d="M14 2H6C4.9 2 4 2.9 4 4V20C4 21.1 4.89 22 5.99 22H18C19.1 22 20 21.1 20 20V8L14 2ZM18 20H6V4H13V9H18V20ZM9 13V15H15V13H9ZM9 16V18H13V16H9Z"
      :fill="currentColor"
    />
    
    <!-- Arrow Right Icon -->
    <path
      v-if="name === 'arrow-right'"
      d="M8.59 16.59L13.17 12L8.59 7.41L10 6L16 12L10 18L8.59 16.59Z"
      :fill="currentColor"
    />
    
    <!-- Refresh Icon -->
    <path
      v-if="name === 'refresh'"
      d="M12 4V1L8 5L12 9V6C15.31 6 18 8.69 18 12C18 15.31 15.31 18 12 18C8.69 18 6 15.31 6 12H4C4 16.42 7.58 20 12 20C16.42 20 20 16.42 20 12C20 7.58 16.42 4 12 4Z"
      :fill="currentColor"
    />
  </svg>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  name: 'profile' | 'brands' | 'globe' | 'match' | 'summary' | 'arrow-right' | 'refresh';
  size?: number;
  color?: string;
}

const props = withDefaults(defineProps<Props>(), {
  size: 24,
  color: 'currentColor'
});

const iconClasses = computed(() => [
  'flex-shrink-0 transition-colors duration-200'
]);

const currentColor = computed(() => props.color);
</script>