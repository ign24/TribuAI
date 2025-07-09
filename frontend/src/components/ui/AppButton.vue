<template>
  <button
    :class="buttonClasses"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <div v-if="loading" class="loading-spinner"></div>
    <span :class="{ 'opacity-0': loading }">
      <slot />
    </span>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  variant?: 'primary' | 'secondary' | 'accent';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  disabled: false,
  loading: false,
  fullWidth: false
});

const emit = defineEmits<{
  click: [event: MouseEvent];
}>();

const buttonClasses = computed(() => [
  'relative inline-flex items-center justify-center font-medium rounded-lg transition-all duration-200',
  'focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-900',
  'disabled:opacity-50 disabled:cursor-not-allowed',
  'transform hover:scale-[1.02] active:scale-[0.98]',
  {
    // Variants
    'bg-tribal-lime text-gray-900 hover:bg-tribal-lime/90 focus:ring-tribal-lime shadow-lg shadow-tribal-lime/25': props.variant === 'primary',
    'bg-slate-blue text-white hover:bg-slate-blue/90 focus:ring-slate-blue shadow-lg shadow-slate-blue/25': props.variant === 'secondary',
    'bg-rust-red text-white hover:bg-rust-red/90 focus:ring-rust-red shadow-lg shadow-rust-red/25': props.variant === 'accent',
    
    // Sizes
    'px-3 py-1.5 text-sm': props.size === 'sm',
    'px-4 py-2 text-base': props.size === 'md',
    'px-6 py-3 text-lg': props.size === 'lg',
    
    // Width
    'w-full': props.fullWidth
  }
]);

const handleClick = (event: MouseEvent) => {
  if (!props.disabled && !props.loading) {
    emit('click', event);
  }
};
</script>

<style scoped>
.loading-spinner {
  @apply absolute inset-0 flex items-center justify-center;
}

.loading-spinner::after {
  @apply w-4 h-4 border-2 border-current border-t-transparent rounded-full;
  content: '';
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>