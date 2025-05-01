import {SkeletonText, Table} from "@chakra-ui/react"


const PendingKisiler = () => (
    <Table.Root size={{base: "sm", md: "md"}}>
        <Table.Header>
            <Table.Row>
                <Table.ColumnHeader w="sm">Kimlik No</Table.ColumnHeader>
                <Table.ColumnHeader w="sm">Adı</Table.ColumnHeader>
                <Table.ColumnHeader w="sm">Soyadı</Table.ColumnHeader>
                <Table.ColumnHeader w="sm">Akrif</Table.ColumnHeader>
            </Table.Row>
        </Table.Header>
        <Table.Body>
            {[...Array(5)].map((_, index) => (
                <Table.Row key={index}>
                    <Table.Cell>
                        <SkeletonText noOfLines={1}/>
                    </Table.Cell>
                    <Table.Cell>
                        <SkeletonText noOfLines={1}/>
                    </Table.Cell>
                    <Table.Cell>
                        <SkeletonText noOfLines={1}/>
                    </Table.Cell>
                    <Table.Cell>
                        <SkeletonText noOfLines={1}/>
                    </Table.Cell>
                </Table.Row>
            ))}
        </Table.Body>
    </Table.Root>
)

export default PendingKisiler
