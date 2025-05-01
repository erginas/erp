// src/routes/_layout.tsx
import {createRoute, Outlet} from '@tanstack/react-router';
import {rootRoute} from '../routes/__root.tsx';
import Navbar from '@/shared/components/Common/Navbar.tsx';
import Sidebar from '@/shared/components/Common/Sidebar.tsx';
import {Flex} from '@chakra-ui/react';

export function AdminLayout() {
    return (
        <Flex direction="column" h="100vh">
            <Navbar/>
            <Flex flex="1" overflow="hidden">
                <Sidebar/>
                <Flex flex="1" direction="column" p={4} overflowY="auto">
                    <Outlet/>
                </Flex>
            </Flex>
        </Flex>
    );
}

export const layoutRoute = createRoute({
    id: '_layout',
    getParentRoute: () => rootRoute,
    component: AdminLayout,
});


// import {Flex} from "@chakra-ui/react"
// import {createFileRoute, Outlet, redirect} from "@tanstack/react-router"
//
// import Navbar from "@/components/Common/Navbar"
// import Sidebar from "@/components/Common/Sidebar"
// import {isLoggedIn} from "@/hooks/useAuth"
//
// export const Route = createFileRoute("/_layout")({
//     component: Layout,
//     beforeLoad: async () => {
//         if (!isLoggedIn()) {
//             throw redirect({
//                 to: "/login",
//             })
//         }
//     },
// })
//
// function Layout() {
//     return (
//         <Flex direction="column" h="100vh">
//             <Navbar/>
//             <Flex flex="1" overflow="hidden">
//                 <Sidebar/>
//                 <Flex flex="1" direction="column" p={4} overflowY="auto">
//                     <Outlet/>
//                 </Flex>
//             </Flex>
//         </Flex>
//     )
// }
//
// export default Layout