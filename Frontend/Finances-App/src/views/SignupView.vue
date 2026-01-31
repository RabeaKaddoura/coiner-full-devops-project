<script setup>
import { ref } from 'vue'
import api from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')
const error = ref('')

const handleSignup = async () => {
  if (!username.value || !email.value || !password.value) {
    error.value = 'Please fill in all fields.'
    return;
  }
    error.value = ''
    try {
    const res = await api.post('register/', {
      username: username.value,
      email: email.value,
      password: password.value
    });

    if(res.status === 201) {
      router.push({name:'login'})
    } else {
      error.value = 'Error signing up, please try again.'
    }
    } catch(e) {
      console.error('Signup error:', e)
    }
}

const sanitizeUser = () => {
  username.value = username.value.replace(/[<>\/\\{}\[\]]/g, '') 
}

const sanitizeEmail = () => {
  email.value = email.value.replace(/[^a-zA-Z0-9@._\-+]/g, '')
}

</script>



<template>
  <div class="min-h-screen flex items-center justify-center bg-background">
    <div class="bg-surface p-8 rounded-2xl shadow-md w-full max-w-md">
      <h2 class="text-2xl font-semibold mb-6 text-center text-text">Sign Up</h2>

      <form @submit.prevent="handleSignup">
        <div class="mb-4">
          <label class="block text-sm font-medium mb-1 text-text">Username</label>
          <input v-model="username" type="text" @input="sanitizeUser" class="w-full border border-border text-text p-2 rounded" />
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-1 text-text">Email</label>
          <input v-model="email" type="email" @input="sanitizeEmail" class="w-full border border-border text-text p-2 rounded" />
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-1 text-text">Password</label>
          <input v-model="password" type="password" class="w-full border border-border p-2 rounded text-text" />
        </div>

        <div v-if="error" class="text-red-500 text-sm mb-4">{{ error }}</div>

        <button type="submit" class="w-full  text-text bg-surface border border-border rounded text-sm mr-4 p-2 px-4 transition-colors hover:bg-hover-bg hover:text-hover-text">
          Create Account
        </button>
      </form>
    </div>
  </div>
</template>

