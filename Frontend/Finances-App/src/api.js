import axios from "axios"
import { ACCESS_TOKEN } from "./constants";
import { isTokenExpired, tryRefresh, checkLogIn } from "./components/auth";


const api = axios.create({
    baseURL: '__VITE_API_URL__' //saves us the trouble of typing the backend url over and over.
});

api.interceptors.request.use(async (config) => {
    const skipAuthCheck = config.url.includes("token") || config.url.includes("refresh_token"); //filtering login and token refreshing from requiring token (you dont have token before login request)
    const token = localStorage.getItem(ACCESS_TOKEN);

    if (!skipAuthCheck && token && isTokenExpired(token)) {
        const refreshed = await tryRefresh();
        if (!refreshed) {
            throw new axios.Cancel("Token expired and refresh failed");
        }
    }

    const finalToken = localStorage.getItem(ACCESS_TOKEN);
    if (finalToken && !skipAuthCheck) {
        config.headers.Authorization = `Bearer ${finalToken}`;
    }

    return config;
});


//Response interceptor to handle failed refresh redirect
api.interceptors.response.use(
    response => response,
    error => {
        if (axios.isCancel(error) && error.message === "Token expired and refresh failed") {
            localStorage.removeItem(ACCESS_TOKEN)
            localStorage.removeItem(REFRESH_TOKEN)
            localStorage.removeItem(Username)
            localStorage.setItem(isLoggedIn, false)
            checkLogIn.value = false
            router.push('/login');
        }

        return Promise.reject(error);
    }
);

export default api