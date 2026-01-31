import { createRouter, createWebHistory } from "vue-router";
import { ACCESS_TOKEN, REFRESH_TOKEN, Username, isLoggedIn } from '@/constants';
import { isTokenExpired, tryRefresh } from "@/components/auth";
import SignupView from "@/views/SignupView.vue";
import LoginView from "@/views/LoginView.vue";
import HomeView from "@/views/HomeView.vue";

function isAuthenticated() {
    return !!localStorage.getItem(ACCESS_TOKEN);
}

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/signup',
            name: 'signup',
            component: SignupView
        },
        {
            path: '/',
            name: 'login',
            component: LoginView
        },
        {
            path: '/home',
            name: 'home',
            component: HomeView,
            meta: { requiresAuth: true }
        }
    ]
})


router.beforeEach(async (to, from, next) => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (to.meta.requiresAuth) {
        if (!token || isTokenExpired(token)) {
            // Token is missing or expired, try to refresh
            const refreshed = await tryRefresh();
            if (!refreshed) {
                // Refresh failed — redirect to login
                return next({ name: 'login' });
            }
        }
        // Token is valid or successfully refreshed
        return next();
    }

    // Route doesn't require auth
    return next();
});

export default router;