// frontend/src/admin/KisiList.tsx

import {Datagrid, DateField, List, TextField} from 'react-admin';

export const KisiList = () => (
    <List>
        <Datagrid rowClick="edit">
            <TextField source="kimlik_no" label="Kimlik No"/>
            <TextField source="adi" label="Adı"/>
            <TextField source="soyadi" label="Soyadı"/>
            <DateField source="dogum_tarihi" label="Doğum Tarihi"/>
            <TextField source="cinsiyeti" label="Cinsiyeti"/>
            <TextField source="cep_tel" label="Cep Telefonu"/>
        </Datagrid>
    </List>
);
