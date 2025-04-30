// src/main.tsx
import {StrictMode} from "react";
import ReactDOM from "react-dom/client";
import {MutationCache, QueryCache, QueryClient, QueryClientProvider,} from "@tanstack/react-query";
import {createRouter, RouterProvider} from "@tanstack/react-router";

import {ApiError, OpenAPI} from "./client";
import {CustomProvider} from "./components/ui/provider";
import {routeTree} from "./routeTree"; // ← Manuel routeTree
// import { routeTree } from "./routeTree.gen"; // artık kullanılmıyor

// OpenAPI konfigurasyonu
OpenAPI.BASE = import.meta.env.VITE_API_URL as string;
OpenAPI.TOKEN = async () => localStorage.getItem("access_token") || "";

// Ortak API hata yöneticisi
const handleApiError = (error: Error) => {
    if (error instanceof ApiError && [401, 403].includes(error.status)) {
        localStorage.removeItem("access_token");
        // doğrudan tanstack-router üzerinden de navigate edebilirsiniz:
        window.location.href = "/login";
    }
};


// React Query istemcisi
const queryClient = new QueryClient({
    queryCache: new QueryCache({onError: handleApiError}),
    mutationCache: new MutationCache({onError: handleApiError}),
});

// TanStack Router oluşturulması
const router = createRouter({routeTree});

declare module "@tanstack/react-router" {
    interface Register {
        router: typeof router;
    }
}

// Uygulamanın render edilmesi
ReactDOM.createRoot(document.getElementById("root")!).render(
    <StrictMode>
        <CustomProvider>
            <QueryClientProvider client={queryClient}>
                <RouterProvider router={router}/>
            </QueryClientProvider>
        </CustomProvider>
    </StrictMode>
);


// import {MutationCache, QueryCache, QueryClient, QueryClientProvider,} from "@tanstack/react-query"
// import {createRouter, RouterProvider} from "@tanstack/react-router"
//
//
// // @ts-ignore
// import React, {StrictMode} from "react"
//
// // @ts-ignore
// import ReactDOM from "react-dom/client"
// import {routeTree} from "./routeTree.gen"
//
//
// import {ApiError, OpenAPI} from "./client"
// import {CustomProvider} from "./components/ui/provider"
//
// // @ts-ignore
// OpenAPI.BASE = import.meta.env.VITE_API_URL
// OpenAPI.TOKEN = async () => {
//     return localStorage.getItem("access_token") || ""
// }
//
// const handleApiError = (error: Error) => {
//     if (error instanceof ApiError && [401, 403].includes(error.status)) {
//         localStorage.removeItem("access_token")
//         window.location.href = "/login"
//     }
// }
// const queryClient = new QueryClient({
//     queryCache: new QueryCache({
//         onError: handleApiError,
//     }),
//     mutationCache: new MutationCache({
//         onError: handleApiError,
//     }),
// })
//
// const router = createRouter({routeTree})
// declare module "@tanstack/react-router" {
//     interface Register {
//         router: typeof router
//     }
// }
//
// ReactDOM.createRoot(document.getElementById("root")!).render(
//     <StrictMode>
//         <CustomProvider>
//             <QueryClientProvider client={queryClient}>
//                 <RouterProvider router={router}/>
//             </QueryClientProvider>
//         </CustomProvider>
//     </StrictMode>,
// )
