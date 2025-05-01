// src/modules/admin/components/AdminPage.tsx

// @ts-ignore
import React from "react";
import {Container, Flex, Heading, Table,} from "@chakra-ui/react";
import {useQuery, useQueryClient} from "@tanstack/react-query";
import {useNavigate} from "@tanstack/react-router"; // ← global hook
import {adminRoute} from "@/routes/_layout/admin.tsx"; // route id’si için
import type {UserPublic} from "@/client";
import {UsersService} from "@/client";
import AddUser from "@/features/Admin/components/AddUser.tsx";
import PendingUsers from "@/features/Pending/PendingUsers.tsx";
import {UserActionsMenu} from "@/shared/components/Common/UserActionsMenu.tsx";
import {
    PaginationItems,
    PaginationNextTrigger,
    PaginationPrevTrigger,
    PaginationRoot,
} from "@/shared/components/ui/pagination.tsx";
import {z} from "zod";

const PER_PAGE = 5;
// @ts-ignore
const usersSearchSchema = z.object({page: z.number().catch(1)});

function getUsersQueryOptions(page: number) {
    return {
        queryFn: () =>
            UsersService.readUsers({
                skip: (page - 1) * PER_PAGE,
                limit: PER_PAGE,
            }),
        queryKey: ["users", {page}],
    };
}

export default function AdminPage() {
    // 1) Sayfa numarasını route’dan çekiyoruz
    const {page = 1} = adminRoute.useSearch();

    // 2) Global useNavigate hook’u, içinde "from" route.id veriyoruz
    const navigate = useNavigate({from: adminRoute.id});

    const queryClient = useQueryClient();
    const {
        data: result = {data: [], count: 0},
        isLoading,
    } = useQuery(getUsersQueryOptions(page));

    const users = result.data;
    const count = result.count;
    const currentUser = queryClient.getQueryData<UserPublic>([
        "currentUser",
    ]);

    // 3) sayfa değiştirirken relative olarak güncelle
    // @ts-ignore
    const setPage = (p: number) =>
        navigate({
            to: ".",              // aynı route, sadece search param’ı değiştir
            search: (prev) => ({...prev, page: p}),
        });

    if (isLoading) {
        return <PendingUsers/>;
    }

    if (!currentUser) {
        // ekstra koruma
        navigate({to: "/login"});
        return null;
    }

    return (
        <Container maxW="full">
            <Heading size="lg" pt={12}>
                Users Management
            </Heading>
            <AddUser/>
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
                    {users.map((user) => (
                        <Table.Row key={user.id}>
                            <Table.Cell>{user.full_name || "N/A"}</Table.Cell>
                            <Table.Cell>{user.email}</Table.Cell>
                            <Table.Cell>
                                {user.is_superuser ? "Superuser" : "User"}
                            </Table.Cell>
                            <Table.Cell>
                                {user.is_active ? "Active" : "Inactive"}
                            </Table.Cell>
                            <Table.Cell>
                                <UserActionsMenu user={user}/>
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
