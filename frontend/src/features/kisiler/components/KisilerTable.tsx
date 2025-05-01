// src/modules/kisiler/components/KisilerTable.tsx
import {useQuery} from "@tanstack/react-query";
import {useNavigate, useSearch} from "@tanstack/react-router";
import {FiSearch} from "react-icons/fi";
// import {Container, Flex, Heading} from "@chakra-ui/react";
import {Container, Flex, Table,} from "@chakra-ui/react";

import {kisilerRoute} from "../router/kisiRouter.tsx";
import {KisilerService} from "@/features/kisiler/api/KisilerServices.ts";
import PendingKisiler from "./PendingKisiler.tsx";
import {EmptyState} from "@/shared/components/ui/empty-state.tsx";

// import {Body, Cell, ColumnHeader, Header, Row, Table} from '@/components/ui/table';
// Pagination bileşenlerinin doğru şekilde import edilmesi
import {
    PaginationItems,
    PaginationNextTrigger,
    PaginationPrevTrigger,
    PaginationRoot,
} from "@/shared/components/ui/pagination.tsx";
// @ts-ignore
import React from "react";
import {KisiActionsMenu} from "@/features/kisiler/components/KisiActionsMenu.tsx";

// Table bileşenlerinin doğru şekilde import edilmesi


const PER_PAGE = 10;

export default function KisilerTable() {
    console.log("🏗️ mount KisilerTable");

    // const {page = 1} = useSearch<{ page?: number }>({from: kisilerRoute.id});
    const {page = 1} = useSearch({
        from: kisilerRoute.id,
    }) as { page?: number };


    const {data: rawData, isLoading} = useQuery({
        queryKey: ["kisiler", {page}],
        queryFn: async () => {
            console.log("🔎 fetching kisiler, page:", page);
            const result = await KisilerService.readKisiler({
                skip: (page - 1) * PER_PAGE,
                limit: PER_PAGE,
            });
            console.log("✅ kisiler raw response:", result);
            return result;
        },
    });

    // Veri yapısının doğru şekilde işlenmesi
    const kisiler = Array.isArray(rawData) ? rawData : rawData?.data ?? [];
    const count = Array.isArray(rawData) ? kisiler.length : rawData?.count ?? kisiler.length;

    // const setPage = (p: number) =>
    //     navigate({to: ".", search: (prev) => ({...prev, page: p})});

    const navigate = useNavigate({from: kisilerRoute.id});

    const setPage = (p: number) => {
        navigate({
            search: (prev) => ({...prev, page: p}),
        });
    };

    if (isLoading) {
        return <PendingKisiler/>;
    }

    if (kisiler.length === 0) {
        return (
            <EmptyState.Root>
                <EmptyState.Indicator>
                    <FiSearch/>
                </EmptyState.Indicator>
                <EmptyState.Content>
                    <EmptyState.Title>Henüz kayıtlı bir kişi yok</EmptyState.Title>
                    <EmptyState.Description>Yeni kişi ekleyebilirsiniz</EmptyState.Description>
                </EmptyState.Content>
            </EmptyState.Root>
        );
    }
    return (
        <Container maxW="full">
            <Table.Root size={{base: "sm", md: "md"}}>
                <Table.Header>
                    <Table.Row>
                        <Table.ColumnHeader>Full name</Table.ColumnHeader>
                        <Table.ColumnHeader>Email</Table.ColumnHeader>
                        <Table.ColumnHeader>Role</Table.ColumnHeader>
                        <Table.ColumnHeader>Status</Table.ColumnHeader>
                        <Table.ColumnHeader>Actions</Table.ColumnHeader>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {kisiler.map((user) => (
                        <Table.Row key={user.kimlik_no}>
                            <Table.Cell>{user.adi || "N/A"}</Table.Cell>
                            <Table.Cell>{user.soyadi}</Table.Cell>
                            <Table.Cell>
                                {user.is_superuser ? "Superuser" : "User"}
                            </Table.Cell>
                            <Table.Cell>
                                {user.is_active ? "Active" : "Inactive"}
                            </Table.Cell>
                            <Table.Cell>
                                <KisiActionsMenu kisi={user}/>
                            </Table.Cell>
                        </Table.Row>
                    ))}
                </Table.Body>
            </Table.Root>
            <Flex justify="flex-end" mt={4}>
                <PaginationRoot
                    count={count}
                    pageSize={PER_PAGE}
                    onPageChange={({page}) => setPage(page)}
                >
                    <Flex>
                        <PaginationPrevTrigger/>
                        <PaginationItems/>
                        <PaginationNextTrigger/>
                    </Flex>
                </PaginationRoot>
            </Flex>
        </Container>
    );
}