<template>
  <span :class="chipClasses">
    <slot />
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  variant?: 'default' | 'accent' | 'secondary';
  size?: 'sm' | 'md';
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  size: 'md'
});

const chipClasses = computed(() => [
  'inline-flex items-center font-medium rounded-full transition-all duration-200',
  'border backdrop-blur-sm',
  {
    // Variants
    'bg-gray-800/80 border-gray-600 text-soft-white': props.variant === 'default',
    'bg-rust-red/20 border-rust-red/50 text-rust-red': props.variant === 'accent',
    'bg-slate-blue/20 border-slate-blue/50 text-slate-blue': props.variant === 'secondary',
    
    // Sizes
    'px-2 py-1 text-xs': props.size === 'sm',
    'px-3 py-1.5 text-sm': props.size === 'md'
  }
]);
</script>