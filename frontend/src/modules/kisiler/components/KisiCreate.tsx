import {Create, SimpleForm, TextInput} from 'react-admin';

export function KisiCreate() {
    return (
        <Create>
            <SimpleForm>
                <TextInput source="kimlik_no" label="Kimlik No"/>
                <TextInput source="adi" label="Adı"/>
                <TextInput source="soyadi" label="Soyadı"/>
                <TextInput source="cep_tel" label="Cep Telefonu"/>
                <TextInput source="adres" label="Adres"/>
            </SimpleForm>
        </Create>
    );
}