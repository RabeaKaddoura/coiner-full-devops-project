<script setup>
import { Icon } from "@iconify/vue";

defineProps({
walletName: {
type: String,
required: true
},
title: {
    type: String,
    required: true
},
value: {
    type: [Number, String],
    required: true
},
isCustom: {
  type:Boolean,
  default: false 
}
});

const emit = defineEmits(['removeCustom', 'edit']);

function confirmDelete() { //wallet delete confirmation
  if (confirm('Are you sure you want to delete this wallet?')) {
    emit('removeCustom');
  }
}
</script>

<template>
  <div class="bg-surface p-6 rounded-2xl shadow-lg w-full max-w-md ">
    <div class="flex justify-between items-start mb-4">
      <div>
        <p class="text-muted text-sm tracking-wide uppercase">{{ walletName }}</p>
        <p class="text-muted text-xs mt-6">{{ title }}</p>

        <div class="flex items-center gap-1 mt-2.5">
          <img
            src="@/assets/icons/saudi-riyal.svg"
            class="w-4 h-4"
            alt="currency"
          />
          <h1 class="text-2xl font-semibold text-success">
            {{ value }}
          </h1>
        </div>
      </div>
      <div class="flex space-x-2">
        <button v-if="isCustom" @click="confirmDelete">
          <Icon icon="mdi:delete-forever" width="24" height="24" class="text-danger" />
        </button>
        <button @click="$emit('edit')">
          <Icon icon="mdi:edit" width="24" height="24" class="text-text" />
        </button>
      </div>
    </div>
  </div>
</template>