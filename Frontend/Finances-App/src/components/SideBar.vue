<script setup>
import { Icon } from "@iconify/vue";

defineEmits(['changePage']);
</script>

<template>
        <div class="w-50 bg-surface border-r border-border py-30 shadow-[inset_0_1px_4px_rgba(255,255,255,0.05)]">
            <nav class="space-y-10">
                <button class="w-full flex gap-2 px-8 py-2 hover:bg-muted text-text" @click="$emit('changePage', 'dash')"> <Icon icon="mdi:view-dashboard" width="24" height="24"/>  Dashboard</button>
                <button class="w-full flex gap-2 px-8 py-2 hover:bg-muted text-text" @click="$emit('changePage', 'trans')"> <Icon icon="mdi:bank-outline" width="24" height="24" /> Transactions</button> <!-- parameters: emit(event the parent should listen to, the value passed as a parameter)-->
                <button class="w-full flex gap-2 px-8 py-2 hover:bg-muted text-text" @click="$emit('changePage', 'budget')"> <Icon icon="mdi:chart-pie" width="24" height="24" /> Budgets</button>
                <button class="w-full flex gap-2 px-8 py-2 hover:bg-muted text-text" @click="$emit('changePage', 'goals')"> <Icon icon="mdi:target-arrow" width="24" height="24" /> Goals</button> 
                <button class="w-full flex gap-2 px-8 py-2 hover:bg-muted text-text" @click="$emit('changePage', 'reports')"> <Icon icon="mdi:report-areaspline" width="24" height="24" />Reports</button> 
            </nav>
        </div>
</template>

  
    