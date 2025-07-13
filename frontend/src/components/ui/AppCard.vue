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
  'rounded-2xl transition-all duration-200',
  {
    'bg-card border border-default': props.variant === 'default',
    'card-glass': props.variant === 'glass',
    'card-elevated': props.variant === 'elevated',
    'p-4': props.padding === 'sm',
    'p-6': props.padding === 'md',
    'p-8': props.padding === 'lg',
    'card-interactive': props.hover
  }
]);
</script>