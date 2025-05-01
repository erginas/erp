// src/components/ui/empty-state.tsx
import React from "react";
import {Box, Flex, Text} from "@chakra-ui/react";

export const EmptyState = {
    Root: (props: React.PropsWithChildren<{}>) => (
        <Flex align="center" justify="center" p={8}>
            {props.children}
        </Flex>
    ),
    Content: (props: React.PropsWithChildren<{}>) => (
        <Flex direction="column" align="center">
            {props.children}
        </Flex>
    ),
    Indicator: (props: React.PropsWithChildren<{}>) => (
        <Box mb={4}>{props.children}</Box>
    ),
    Title: (props: React.PropsWithChildren<{}>) => (
        <Text fontSize="lg" fontWeight="bold" mb={2}>
            {props.children}
        </Text>
    ),
    Description: (props: React.PropsWithChildren<{}>) => (
        <Text color="gray.500">{props.children}</Text>
    ),
};
