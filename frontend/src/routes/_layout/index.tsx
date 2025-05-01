// src/routes/_layout/index.tsx
import {createRoute} from "@tanstack/react-router";
import {layoutRoute} from "../../app/_layout.tsx";
import Dashboard from "@/features/dashboard/Dashboard"; // şimdi bu import çalışacak

export const dashboardRoute = createRoute({
    path: "/",
    getParentRoute: () => layoutRoute,
    component: Dashboard,
});

// import {Box, Container, Text} from "@chakra-ui/react"
// import {createFileRoute} from "@tanstack/react-router"
//
// import useAuth from "@/hooks/useAuth"
//
// export const Route = createFileRoute("/_layout/")({
//     component: Dashboard,
// })
//
// function Dashboard() {
//     const {user: currentUser} = useAuth()
//
//     return (
//         <>
//             <Container maxW="full">
//                 <Box pt={12} m={4}>
//                     <Text fontSize="2xl" truncate maxW="sm">
//                         Hi, {currentUser?.full_name || currentUser?.email} 👋🏼
//                     </Text>
//                     <Text>Welcome back, nice to see you again!</Text>
//                 </Box>
//             </Container>
//         </>
//     )
// }