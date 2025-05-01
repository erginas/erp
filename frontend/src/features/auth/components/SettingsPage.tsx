// src/modules/settings/components/SettingsPage.tsx

import {Container, Heading, Tabs} from "@chakra-ui/react";
import useAuth from "@/shared/hooks/useAuth.ts";
import Appearance from "@/shared/components/UserSettings/Appearance.tsx";
import ChangePassword from "@/shared/components/UserSettings/ChangePassword.tsx";
import DeleteAccount from "@/shared/components/UserSettings/DeleteAccount.tsx";
import UserInformation from "@/shared/components/UserSettings/UserInformation.tsx";

const tabsConfig = [
    {value: "my-profile", title: "My profile", component: UserInformation},
    {value: "password", title: "Password", component: ChangePassword},
    {value: "appearance", title: "Appearance", component: Appearance},
    {value: "danger-zone", title: "Danger zone", component: DeleteAccount},
];

export default function SettingsPage() {
    const {user: currentUser} = useAuth();

    if (!currentUser) {
        return null;
    }

    const finalTabs = currentUser.is_superuser
        ? tabsConfig.slice(0, 3)
        : tabsConfig;

    return (
        <Container maxW="full">
            <Heading size="lg" textAlign={{base: "center", md: "left"}} py={12}>
                User Settings
            </Heading>

            <Tabs.Root defaultValue="my-profile" variant="subtle">
                <Tabs.List>
                    {finalTabs.map((tab) => (
                        <Tabs.Trigger key={tab.value} value={tab.value}>
                            {tab.title}
                        </Tabs.Trigger>
                    ))}
                </Tabs.List>
                {finalTabs.map((tab) => (
                    <Tabs.Content key={tab.value} value={tab.value}>
                        <tab.component/>
                    </Tabs.Content>
                ))}
            </Tabs.Root>
        </Container>
    );
}
