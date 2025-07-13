<template>
  <header class="sticky top-0 z-50 bg-obsidian/80 backdrop-blur-xl border-b border-default">
    <div class="container mx-auto">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <div class="flex items-center gap-3">
          <img 
            src="/src/assets/logo.png" 
            alt="TribuAI Logo" 
            class="w-20 h-20 object-contain"
            style="width: 120px !important; height: 120px !important;"
          />
        </div>

        <!-- Status Indicator -->
        <div class="flex items-center gap-3">
          <div class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-card border border-tribal-lime/20 shadow-sm shadow-tribal-lime/10">
            <div class="status-online"></div>
            <span class="text-sm font-medium text-gray-300">Online</span>
          </div>
          
          <!-- User Avatar Placeholder -->
          <div class="w-8 h-8 rounded-full bg-gradient-accent flex items-center justify-center shadow-sm shadow-rust-red/20">
            <span class="text-sm font-semibold text-white">U</span>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>