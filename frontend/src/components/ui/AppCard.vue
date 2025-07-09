<template>
  <div :class="cardClasses">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  variant?: 'default' | 'glass' | 'elevated';
  padding?: 'sm' | 'md' | 'lg';
  hover?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'glass',
  padding: 'md',
  hover: false
});

const cardClasses = computed(() => [
  'rounded-xl transition-all duration-200',
  {
    // Variants
    'bg-warm-gray border border-gray-700': props.variant === 'default',
    'bg-warm-gray/80 backdrop-blur-md border border-gray-700/50 shadow-lg': props.variant === 'glass',
    'bg-warm-gray shadow-2xl shadow-black/40 border border-gray-600': props.variant === 'elevated',
    
    // Padding
    'p-3': props.padding === 'sm',
    'p-6': props.padding === 'md',
    'p-8': props.padding === 'lg',
    
    // Hover effects
    'hover:shadow-xl hover:shadow-black/30 hover:transform hover:scale-[1.02]': props.hover
  }
]);
</script>