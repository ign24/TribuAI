<template>
  <span :class="chipClasses">
    <slot />
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  variant?: 'default' | 'primary' | 'secondary' | 'accent' | 'success';
  size?: 'sm' | 'md';
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  size: 'md'
});

const chipClasses = computed(() => [
  'chip',
  {
    'chip-default': props.variant === 'default',
    'chip-primary': props.variant === 'primary',
    'chip-success': props.variant === 'success',
    'chip-accent': props.variant === 'accent',
  }
]);
</script>