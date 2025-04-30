import {createRoute, redirect} from "@tanstack/react-router";
import {rootRoute} from "@/routes/__root";
import LoginPage from "../components/LoginPage";
import {isLoggedIn} from "@/hooks/useAuth";

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
