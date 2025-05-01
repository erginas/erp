// features/hr/pages/KisiListPage.tsx
// @ts-ignore
import React, { useState } from 'react';
import { useKisiler, useCreateKisi, useUpdateKisi, useDeleteKisi } from '../api/useKisiler';
import { DataGrid } from '../../../shared/components/DataGrid';
import { KisiForm } from '../components/KisiForm';
import { Kisi } from '../types/kisi';
import {Button} from "@/shared/components/ui/button.tsx";
import { ColDef } from 'ag-grid-community'



export default function KisiListPage() {
  const { data = [], isLoading } = useKisiler();
  const kisiler: Kisi[] = data ?? [];
  const createKisi = useCreateKisi();
  const updateKisi = useUpdateKisi();
  const deleteKisi = useDeleteKisi();
  const [editing, setEditing] = useState<Kisi | null>(null);
  const [showForm, setShowForm] = useState(false);




  if (isLoading) return <div>Yükleniyor...</div>;

  const columns: ColDef[] = [
    { field: 'kimlik_no', headerName: 'KIMLIK_NO' },
    { field: 'adi', headerName: 'ADI' },
    { field: 'soyadi', headerName: 'SOYADI' },
    { field: 'baba_adi', headerName: 'BABA_ADI' },
    { field: 'ana_adi', headerName: 'ANA_ADI' },
    { field: 'meslegi', headerName: 'MESLEGI' },
    { field: 'dogum_yeri', headerName: 'DOGUM_YERI' },
    { field: 'kan_grubu', headerName: 'KAN_GRUBU' },
    { field: 'cinsiyeti', headerName: 'CINSIYETI' },
    { field: 'medeni_hali', headerName: 'MEDENI_HALI' },
    { field: 'ev_tel', headerName: 'EV_TEL' },
    { field: 'cep_tel', headerName: 'CEP_TEL' },
    { field: 'is_tel', headerName: 'IS_TEL' },
    { field: 'adres', headerName: 'ADRES' },
    { field: 'sirket', headerName: 'ILGILI_SIRKET' },
    { field: 'isten_cikis_t', headerName: 'ISTEN_CIKIS_T' },
    { field: 'gorevi', headerName: 'GOREVI' },
    { field: 'mesai_fl', headerName: 'MESAI_FL' },
    { field: 'egitim_durumu', headerName: 'EGITIM_DURUMU' },
    { field: 'dogum_ay', headerName: 'DOGUM_AY' },
    { field: 'dogum_yil', headerName: 'DOGUM_YIL' },
    { field: 'org_adi', headerName: 'ORG_ADI' },
    { field: 'gorev_adi', headerName: 'GOREV_ADI' },
    { field: 'ssk_no', headerName: 'SSK_NO' },
    { field: 'ise_giris_tarihi', headerName: 'ISE_GIRIS_TARIHI' },
   {
    headerName: 'Actions',
    cellRendererFramework: params => (
      <div className="flex space-x-2">
        <Button onClick={() => { setEditing(params.data); setShowForm(true); }}>
          Düzenle
        </Button>
        <Button variant="destructive"
                onClick={() => deleteKisi.mutate(params.data.KIMLIK_NO)}>
          Sil
        </Button>
      </div>
    ),
  },
]

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Kişi Listesi</h1>
      <Button onClick={() => { setEditing(null); setShowForm(true); }} className="mb-4">Yeni Kişi</Button>
      {showForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
          <div className="bg-white p-6 rounded shadow-lg w-96">
            <KisiForm
              initialData={editing || undefined}
              onSubmit={data => {
                editing ? updateKisi.mutate({ KIMLIK_NO: editing.KIMLIK_NO, ...data }) : createKisi.mutate(data);
                setShowForm(false);
                setEditing(null);
              }}
              onCancel={() => setShowForm(false)}
            />
          </div>
        </div>
      )}
      <DataGrid rows={kisiler} columns={columns} />
    </div>
  );
}