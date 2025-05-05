import {rootRoute} from '@/routes/__root';
import {layoutRoute} from '@/app/_layout.tsx';
import {recoverPasswordRoute} from '@/routes/recover-password';
import {resetPasswordRoute} from '@/routes/reset-password';
import {signupRoute} from '@/routes/signup';
import {dashboardRoute} from '@/routes/_layout/index';
import {adminRoute} from '@/routes/_layout/admin';
// import {itemsRoute} from '@/routes/_layout/items';
import {settingsRoute} from '@/routes/_layout/settings';

import {loginRoute} from "@/features/auth/router/loginRoute";
import {kisilerRoute} from "@/features/kisiler/router/kisiRouter.tsx";

export const routeTree_ol = rootRoute.addChildren([
    layoutRoute.addChildren([
        dashboardRoute,
        adminRoute,
        // itemsRoute,

        settingsRoute,
        kisilerRoute,
    ]),
    loginRoute,
    recoverPasswordRoute,
    resetPasswordRoute,
    signupRoute,
]);
