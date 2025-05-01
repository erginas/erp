// src/modules/dashboard/Dashboard.tsx
import {Box, Container, Text} from "@chakra-ui/react";
import useAuth from "@/shared/hooks/useAuth.ts";

export default function Dashboard() {
    const {user: currentUser} = useAuth();

    return (
        <Container maxW="full">
            <Box pt={12} m={4}>
                <Text fontSize="2xl" truncate maxW="sm">
                    Hi, {currentUser?.full_name || currentUser?.email} 👋🏼
                </Text>
                <Text>Welcome back, nice to see you again!</Text>
            </Box>
        </Container>
    );
}
