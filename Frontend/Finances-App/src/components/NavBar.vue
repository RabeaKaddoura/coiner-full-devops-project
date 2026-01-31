<script setup>
import money from '../assets/img/icons8-money-48.png';
import { useRouter } from 'vue-router';
import { checkLogIn } from './auth.js';
import { REFRESH_TOKEN, ACCESS_TOKEN, Username, isLoggedIn } from '@/constants';

const router = useRouter()

const routeLogin = () => {
  // Navigate to signup page
  router.push({ name: 'login' })
}

const handleLogOut = () => {
    
if (confirm('Are you sure you want to logout?')) {
    localStorage.removeItem(ACCESS_TOKEN)
    localStorage.removeItem(REFRESH_TOKEN)
    localStorage.removeItem(Username)
    localStorage.setItem(isLoggedIn, false)
    checkLogIn.value = false
    router.push({ name: 'login' })
 }
}
</script>

<template>
    <nav class="bg-surface border-b">
        <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
            <div class="flex h-20 items-center justify-between">
                <div class="flex flex-1 items-center justify-center md:items-stretch md:justify-start">
                    <!-- Logo (wrapped in link)-->
                    <a class="flex flex-shrink-0 items-center mr-4" href="#">
                        <img class="h-10 w-auto" :src="money" alt="Coiner Logo" />
                        <span class="hidden md:block text-white text-2xl font-bold ml-2">Coiner</span>
                    </a>
                    <!--Buttons-->   
                    <div class="ml-auto">
                        <div class="flex space-x-2">
                           <button
                            v-if="checkLogIn"
                            @click="handleLogOut"
                            class="text-text bg-surface border border-border rounded text-sm  p-2 px-4 transition-colors hover:bg-hover-bg hover:text-hover-text"
                            >
                            Logout
                            </button>


                            <button v-else @click="routeLogin" class="text-text bg-surface border border-border rounded text-sm mr-4 p-2 px-4 transition-colors hover:bg-hover-bg hover:text-hover-text">
                                    Login
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </nav>
</template>