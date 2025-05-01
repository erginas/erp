import {createRoute, redirect} from "@tanstack/react-router";
import {rootRoute} from "@/routes/__root.tsx";
import LoginPage from "../components/LoginPage.tsx";
import {isLoggedIn} from "@/shared/hooks/useAuth.ts";

export const loginRoute = createRoute({
    path: "/login",
    getParentRoute: () => rootRoute,
    component: LoginPage,
    beforeLoad: async () => {
        // eğer zaten login ise dashboard'a at
        if (isLoggedIn()) {
            throw redirect({to: "/"});
        }
    },
});
