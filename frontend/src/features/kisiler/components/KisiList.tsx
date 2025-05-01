// src/modules/kisiler/components/KisiList.tsx

import {
    CreateButton,
    Datagrid,
    DateField,
    ExportButton,
    List,
    TextField,
    TextInput,
    TopToolbar,
    useListContext,
} from "react-admin";
import {Box} from "@mui/material";

/**
 * Filtre Alanları
 */
const KisiFilters = [
    <TextInput label="Adı" source="adi" alwaysOn/>,
    <TextInput label="Soyadı" source="soyadi"/>,
    <TextInput label="Cep Tel" source="cep_tel"/>,
];

const ListActions = () => {
    const {total} = useListContext();
    return (
        <TopToolbar>
            {total > 0 && <ExportButton/>}
            <CreateButton/>
        </TopToolbar>
    );
};

/**
 * Ana Liste Component
 */
export const KisiList = () => {
    return (
        <Box sx={{padding: 2}}>
            <List filters={KisiFilters} actions={<ListActions/>} perPage={10}>
                <Datagrid rowClick="edit">
                    <TextField source="kimlik_no" label="Kimlik No"/>
                    <TextField source="adi" label="Adı"/>
                    <TextField source="soyadi" label="Soyadı"/>
                    <TextField source="cep_tel" label="Cep Telefonu"/>
                    <DateField source="dogum_tarihi" label="Doğum Tarihi"/>
                    <TextField source="adres" label="Adres"/>
                    <TextField source="aktif" label="Aktif"/>
                </Datagrid>
            </List>
        </Box>
    );
};
