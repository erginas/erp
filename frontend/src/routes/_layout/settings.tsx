// src/routes/_layout/settings.tsx

import {createRoute, redirect} from "@tanstack/react-router";
import {layoutRoute} from "../../app/_layout.tsx";
// import {
//   Container,
//   Heading,
//   Tabs,
// } from "@chakra-ui/react";
// Component’i ayrı dosyada tutun; burada yalnızca route tanımı var:
import SettingsPage from "@/features/auth/components/SettingsPage";

// Basit bir doğrulama fonksiyonu:
function isLoggedInSync(): boolean {
    // Örnek: token’ı localStorage’dan oku
    return Boolean(localStorage.getItem("access_token"));
}

export const settingsRoute = createRoute({
    path: "settings",                // Layout altında "/settings"
    getParentRoute: () => layoutRoute,
    component: SettingsPage,
    beforeLoad: async () => {
        if (!isLoggedInSync()) {
            // Login değilse /login’e yönlendir
            throw redirect({to: "/login"});
        }
    },
});


// import {Container, Heading, Tabs} from "@chakra-ui/react"
// import {createFileRoute} from "@tanstack/react-router"
//
// import Appearance from "@/components/UserSettings/Appearance"
// import ChangePassword from "@/components/UserSettings/ChangePassword"
// import DeleteAccount from "@/components/UserSettings/DeleteAccount"
// import UserInformation from "@/components/UserSettings/UserInformation"
// import useAuth from "@/hooks/useAuth"
//
// const tabsConfig = [
//     {value: "my-profile", title: "My profile", component: UserInformation},
//     {value: "password", title: "Password", component: ChangePassword},
//     {value: "appearance", title: "Appearance", component: Appearance},
//     {value: "danger-zone", title: "Danger zone", component: DeleteAccount},
// ]
//
// export const Route = createFileRoute("/_layout/settings")({
//     component: UserSettings,
// })
//
// function UserSettings() {
//     const {user: currentUser} = useAuth()
//     const finalTabs = currentUser?.is_superuser
//         ? tabsConfig.slice(0, 3)
//         : tabsConfig
//
//     if (!currentUser) {
//         return null
//     }
//
//     return (
//         <Container maxW="full">
//             <Heading size="lg" textAlign={{base: "center", md: "left"}} py={12}>
//                 User Settings
//             </Heading>
//
//             <Tabs.Root defaultValue="my-profile" variant="subtle">
//                 <Tabs.List>
//                     {finalTabs.map((tab) => (
//                         <Tabs.Trigger key={tab.value} value={tab.value}>
//                             {tab.title}
//                         </Tabs.Trigger>
//                     ))}
//                 </Tabs.List>
//                 {finalTabs.map((tab) => (
//                     <Tabs.Content key={tab.value} value={tab.value}>
//                         <tab.component/>
//                     </Tabs.Content>
//                 ))}
//             </Tabs.Root>
//         </Container>
//     )
// }