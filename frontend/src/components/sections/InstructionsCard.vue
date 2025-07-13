<template>
  <div class="card-glass rounded-2xl p-6">
    <div class="text-center mb-6">
      <h3 class="text-lg font-semibold text-soft-white mb-2">How TribuAI Works</h3>
      <p class="text-sm text-gray-400">Discover your cultural identity in 3 simple steps</p>
    </div>

    <div class="space-y-4">
      <!-- Step 1 -->
      <div class="flex items-start gap-4 p-4 rounded-xl bg-gradient-to-r from-tribal-lime/5 to-transparent border border-tribal-lime/20">
        <div class="w-8 h-8 rounded-full bg-gradient-neon flex items-center justify-center flex-shrink-0 shadow-sm shadow-tribal-lime/20">
          <span class="text-sm font-bold text-white">1</span>
        </div>
        <div>
          <h4 class="font-semibold text-soft-white text-sm mb-1">Share Your Preferences</h4>
          <p class="text-xs text-gray-400 leading-relaxed">
            Tell us about your music taste, style preferences, values, and interests. Be as detailed as you like!
          </p>
        </div>
      </div>

      <!-- Step 2 -->
      <div class="flex items-start gap-4 p-4 rounded-xl bg-gradient-to-r from-slate-blue/5 to-transparent border border-slate-blue/20">
        <div class="w-8 h-8 rounded-full bg-gradient-accent flex items-center justify-center flex-shrink-0 shadow-sm shadow-rust-red/20">
          <span class="text-sm font-bold text-white">2</span>
        </div>
        <div>
          <h4 class="font-semibold text-soft-white text-sm mb-1">AI Analysis</h4>
          <p class="text-xs text-gray-400 leading-relaxed">
            Our cultural intelligence analyzes your input to identify patterns and create your unique cultural profile.
          </p>
        </div>
      </div>

      <!-- Step 3 -->
      <div class="flex items-start gap-4 p-4 rounded-xl bg-gradient-to-r from-rust-red/5 to-transparent border border-rust-red/20">
        <div class="w-8 h-8 rounded-full bg-gradient-success flex items-center justify-center flex-shrink-0 shadow-sm shadow-tribal-lime/20">
          <span class="text-sm font-bold text-white">3</span>
        </div>
        <div>
          <h4 class="font-semibold text-soft-white text-sm mb-1">Get Recommendations</h4>
          <p class="text-xs text-gray-400 leading-relaxed">
            Receive personalized brand recommendations, geographic affinities, and cultural compatibility matches.
          </p>
        </div>
      </div>
    </div>

    <!-- What to Include Section -->
    <div class="mt-6 p-4 rounded-xl bg-gradient-to-r from-gray-800/30 to-gray-700/20 border border-gray-700/50">
      <h4 class="font-semibold text-soft-white text-sm mb-3 flex items-center gap-2">
        <span class="w-4 h-4 rounded-full bg-tribal-lime"></span>
        What to Include
      </h4>
      <div class="grid grid-cols-2 gap-3 text-xs">
        <div class="space-y-2">
          <div class="flex items-center gap-2 text-gray-300">
            <div class="w-1.5 h-1.5 bg-tribal-lime rounded-full"></div>
            <span>Music genres you love</span>
          </div>
          <div class="flex items-center gap-2 text-gray-300">
            <div class="w-1.5 h-1.5 bg-slate-blue rounded-full"></div>
            <span>Fashion & style preferences</span>
          </div>
          <div class="flex items-center gap-2 text-gray-300">
            <div class="w-1.5 h-1.5 bg-rust-red rounded-full"></div>
            <span>Core values & beliefs</span>
          </div>
        </div>
        <div class="space-y-2">
          <div class="flex items-center gap-2 text-gray-300">
            <div class="w-1.5 h-1.5 bg-tribal-lime rounded-full"></div>
            <span>Hobbies & interests</span>
          </div>
          <div class="flex items-center gap-2 text-gray-300">
            <div class="w-1.5 h-1.5 bg-slate-blue rounded-full"></div>
            <span>Art & creative preferences</span>
          </div>
          <div class="flex items-center gap-2 text-gray-300">
            <div class="w-1.5 h-1.5 bg-rust-red rounded-full"></div>
            <span>Lifestyle choices</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Privacy Note -->
    <div class="mt-4 text-center">
      <p class="text-xs text-gray-400">
        <span class="inline-flex items-center gap-1">
          🔒 Privacy first • Your data stays secure
        </span>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
// Instructions component - no props needed
</script>