import { jwtDecode } from 'jwt-decode';
import axios from 'axios';
import { ACCESS_TOKEN, REFRESH_TOKEN, isLoggedIn } from '@/constants';
import { ref } from 'vue'
import router from '@/router';

export const checkLogIn = ref(localStorage.getItem(isLoggedIn) === 'true') //login status


export function isTokenExpired(token) { //checks if token is expired
    try {
        const decoded = jwtDecode(token); //decoding token to extract info like expiration
        const now = Date.now() / 1000; //to seconds
        return decoded.exp < now; //returns true if token is expired. otherwise returns false
    } catch {
        return true; //if there's an issue we automatically assume token is expired.
    }
}


export async function tryRefresh() { //attempting to refresh token
    const refresh = localStorage.getItem(REFRESH_TOKEN);
    if (!refresh) {
        return false;
    }
    try {
        const res = await axios.post('http://localhost:8000/api/refresh_token/', { refresh });
        if (res.status === 200) {
            localStorage.setItem(ACCESS_TOKEN, res.data.access);
            return true;
        }
    } catch (e) {
        console.error('Refresh token error:', e)
        localStorage.removeItem(ACCESS_TOKEN)
        localStorage.removeItem(REFRESH_TOKEN)
        localStorage.removeItem(Username)
        localStorage.setItem(isLoggedIn, false)
    }
    return false;
}

export async function checkAuth() { //checking token for requests. if expired or non are found, we attempt refreshing. otherwise user goes to login screen. returns true = authorized. false = not authorized
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (!token || isTokenExpired(token)) { //token expired. try refreshing it.
        const refreshed = await tryRefresh();
        if (refreshed) {
            return true; //refresh successful
        } else {
            router.push({ name: 'login' }); //refresh failed. you need to log-in again.
            return false;
        }
    } else {
        return true; //authorized, proceed. 
    }
}