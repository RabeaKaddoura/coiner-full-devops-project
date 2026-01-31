<script setup>
import { ACCESS_TOKEN, REFRESH_TOKEN, Username, isLoggedIn } from '@/constants';
import { ref } from 'vue'
import { useRouter } from 'vue-router';
import api from '@/api';
import { checkLogIn } from '@/components/auth.js';

const router = useRouter()

const username = ref('')
const password = ref('')
const error = ref('')

const handleLogin = async () => {
  if (!username.value || !password.value) {
    error.value = 'Please fill in all fields.'
    return
  }
    error.value = ''
    try {
    const res = await api.post('token/', {
      username: username.value,
      password: password.value
    });

    if(res.status === 200) {
      localStorage.setItem(ACCESS_TOKEN, res.data.access);
      localStorage.setItem(REFRESH_TOKEN, res.data.refresh)
      localStorage.setItem(Username, res.data.username)
      localStorage.setItem(isLoggedIn, true)
      checkLogIn.value = true
      router.push({name: 'home'})
    } else {
      error.value = 'Error logging in, please try again.'

    }
    } catch(e) {
      console.error('Login error:', e)
      error.value = 'Error logging in. Please try again.'
    }
  
}

const routeSignup = () => {
  router.push({name:'signup'})
}

const sanitizeInput = () => {
  username.value = username.value.replace(/[<>\/\\{}\[\]]/g, '')
}



/** const handleGuest = () => {
localStorage.removeItem(ACCESS_TOKEN)
localStorage.removeItem(REFRESH_TOKEN)
localStorage.removeItem(Username)
localStorage.setItem(isLoggedIn, false)
checkLogIn.value = false
  router.push({name:'home'})
} */

</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-background">
    <div class="bg-surface p-8 rounded-2xl shadow-md w-full max-w-md border border-black">
      <h2 class="text-2xl font-semibold mb-6 text-center text-text">Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block text-sm font-medium mb-1 text-text">Username</label>
          <input v-model="username" type="text" @input="sanitizeInput" class="w-full border border-border text-text p-2 rounded" />
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium mb-1 text-text">Password</label>
          <input v-model="password" type="password" class="w-full border border-border text-text p-2 rounded" />
        </div>
        <div v-if="error" class="text-red-500 text-sm mb-4">{{ error }}</div>
        <button type="submit" class="w-full text-text bg-surface border border-border rounded text-sm mr-4 p-2 px-4 transition-colors hover:bg-hover-bg hover:text-hover-text">
          Sign In
        </button>
      </form>
      <div class="mt-6 ml-4 text-center">
        <button @click="routeSignup" class="text-text hover:text-muted text-sm mr-4 text-center">
          Signup
        </button>
      </div>
    </div>
  </div>
</template>