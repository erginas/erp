import {Container, EmptyState, Flex, Heading, Table, VStack,} from "@chakra-ui/react"
import {useQuery} from "@tanstack/react-query"
import {createFileRoute, useNavigate} from "@tanstack/react-router"
import {FiSearch} from "react-icons/fi"
import {z} from "zod"


import {KisilerService} from "../../modules/kisiler/api/KisilerServices"
import AddKisi from "../../modules/kisiler/components/AddKisi"

import {KisiActionsMenu} from "../../components/Common/KisiActionsMenu"

import PendingKisiler from "../../components/Pending/PendingKisiler"
import {
    PaginationItems,
    PaginationNextTrigger,
    PaginationPrevTrigger,
    PaginationRoot,
} from "../../components/ui/pagination"

const kisiSearchSchema = z.object({
    page: z.number().catch(1),
})

const PER_PAGE = 5

function getKisiQueryOptions({page}: { page: number }) {
    return {
        queryFn: () =>
            KisilerService.readKisiler({skip: (page - 1) * PER_PAGE, limit: PER_PAGE}),
        queryKey: ["kisiler", {page}],
    }
    
}

export const Route = createFileRoute("/_layout/kisiler")({
    component: Kisiler,
    validateSearch: (search) => kisiSearchSchema.parse(search),
})

function KisiTable() {
    const navigate = useNavigate({from: Route.fullPath})
    const {page} = Route.useSearch()

    const {data, isLoading, isPlaceholderData} = useQuery({
        ...getKisiQueryOptions({page}),
        placeholderData: (prevData) => prevData,
    })

    const setPage = (page: number) =>
        navigate({
            search: (prev: { [key: string]: string }) => ({...prev, page}),
        })

    console.log("enignden selamlar", data ?? [])
    const kisi = data?.data.slice(0, PER_PAGE) ?? []
    const count = data?.count ?? 0

    if (isLoading) {
        return <PendingKisiler/>
    }

    if (kisi.length === 0) {
        return (
            <EmptyState.Root>
                <EmptyState.Content>
                    <EmptyState.Indicator>
                        <FiSearch/>
                    </EmptyState.Indicator>
                    <VStack textAlign="center">
                        <EmptyState.Title>You don't have any items yet</EmptyState.Title>
                        <EmptyState.Description>
                            Add a new item to get started
                        </EmptyState.Description>
                    </VStack>
                </EmptyState.Content>
            </EmptyState.Root>
        )
    }

    return (
        <>
            <Table.Root size={{base: "sm", md: "md"}}>
                <Table.Header>
                    <Table.Row>
                        <Table.ColumnHeader w="sm">Kimlik NO</Table.ColumnHeader>
                        <Table.ColumnHeader w="sm">Adı</Table.ColumnHeader>
                        <Table.ColumnHeader w="sm">Soyadı</Table.ColumnHeader>
                        <Table.ColumnHeader w="sm">Aktif</Table.ColumnHeader>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {kisi?.map((kisi) => (
                        <Table.Row key={kisi.kimlik_no} opacity={isPlaceholderData ? 0.5 : 1}>
                            <Table.Cell truncate maxW="sm">
                                {kisi.kimlik_no}
                            </Table.Cell>
                            <Table.Cell truncate maxW="sm">
                                {kisi.adi}
                            </Table.Cell>
                            <Table.Cell
                                color={!kisi.soyadi ? "gray" : "inherit"}
                                truncate
                                maxW="30%"
                            >
                                {kisi.soyadi || "N/A"}
                            </Table.Cell>
                            <Table.Cell>
                                <KisiActionsMenu kisi={kisi}/>
                            </Table.Cell>
                        </Table.Row>
                    ))}
                </Table.Body>
            </Table.Root>
            <Flex justifyContent="flex-end" mt={4}>
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
        </>
    )
}

function Kisiler() {
    return (
        <Container maxW="full">
            <Heading size="lg" pt={12}>
                Kişiler Management
            </Heading>
            <AddKisi/>
            <KisiTable/>
        </Container>
    )
}