// features/hr/pages/KisiListPage.tsx
import {useCallback, useState} from 'react'
import {useKisiler} from '../api/useKisiler'
import {DataGrid} from '@/shared/components/DataGrid/DataGrid'
import {Input} from '@/shared/components/ui/Input'
import {Button} from '@/shared/components/ui/button'
import {Card, CardBody, CardHeader} from '@/shared/components/ui/Card'
import {Plus} from 'lucide-react'
import {ColDef} from "ag-grid-community";

export default function KisiListPage() {
    const [page, setPage] = useState(0)
    const [searchTerm, setSearchTerm] = useState('')
    const [search, setSearch] = useState('')
    const pageSize = 20

    const {data: kisiList = [], isLoading, isError} = useKisiler({page, pageSize, search})

    const handleSearch = useCallback(() => {
        setPage(0)
        setSearch(searchTerm)
    }, [searchTerm])

    const columns: ColDef[] = [
        {field: 'kimlik_no', headerName: 'KIMLIK_NO'},
        {field: 'adi', headerName: 'ADI'},
        {field: 'soyadi', headerName: 'SOYADI'},
        {field: 'baba_adi', headerName: 'BABA_ADI'},
        {field: 'ana_adi', headerName: 'ANA_ADI'},
        {field: 'meslegi', headerName: 'MESLEGI'},
        {field: 'dogum_yeri', headerName: 'DOGUM_YERI'},
        {field: 'kan_grubu', headerName: 'KAN_GRUBU'},
        {field: 'cinsiyeti', headerName: 'CINSIYETI'},
        {field: 'medeni_hali', headerName: 'MEDENI_HALI'},
        {field: 'ev_tel', headerName: 'EV_TEL'},
        {field: 'cep_tel', headerName: 'CEP_TEL'},
        {field: 'is_tel', headerName: 'IS_TEL'},
        {field: 'adres', headerName: 'ADRES'},
        {field: 'sirket', headerName: 'ILGILI_SIRKET'},
        {field: 'isten_cikis_t', headerName: 'ISTEN_CIKIS_T'},
        {field: 'gorevi', headerName: 'GOREVI'},
        {field: 'mesai_fl', headerName: 'MESAI_FL'},
        {field: 'egitim_durumu', headerName: 'EGITIM_DURUMU'},
        {field: 'dogum_ay', headerName: 'DOGUM_AY'},
        {field: 'dogum_yil', headerName: 'DOGUM_YIL'},
        {field: 'org_adi', headerName: 'ORG_ADI'},
        {field: 'gorev_adi', headerName: 'GOREV_ADI'},
        {field: 'ssk_no', headerName: 'SSK_NO'},
        {field: 'ise_giris_tarihi', headerName: 'ISE_GIRIS_TARIHI'},
        {
            headerName: 'Actions',
            cellRenderer: params => (
                <div className="flex space-x-2">
                    <Button onClick={() => {/* edit */
                    }}>Düzenle</Button>
                    <Button variant="destructive" onClick={() => {/* delete */
                    }}>Sil</Button>
                </div>
            )
        }
    ]

    if (isLoading) return <div className="text-center py-10">Yükleniyor...</div>
    if (isError) return <div className="text-center py-10 text-red-600">Veri yüklenemedi.</div>

    // Handle enter press for search
    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') {
            setPage(0)
            setSearch(searchTerm)
        }
    }

    return (
        <Card className="m-4 bg-white shadow-md">
            <CardHeader
                className="flex flex-col md:flex-row md:justify-between md:items-center space-y-4 md:space-y-0 p-4">
                <h1 className="text-2xl font-bold text-gray-900">Kişi Yönetimi</h1>
                <div className="flex items-center space-x-2">
                    <Input
                        placeholder="Ara… (adi:Ahmet veya genel)"
                        value={searchTerm}
                        onChange={e => setSearchTerm(e.target.value)}
                        onKeyDown={e => e.key === 'Enter' && handleSearch()}
                        className="max-w-xs"
                    />
                    <Button onClick={handleSearch}>Ara</Button>
                    <Button variant="primary" onClick={() => {/* open add modal */
                    }}>
                        <Plus size={16} className="mr-1"/> Yeni Kişi
                    </Button>
                </div>
            </CardHeader>
            <CardBody className="p-4">

                {isLoading && <div className="text-center py-10">Yükleniyor...</div>}
                {isError && <div className="text-center py-10 text-red-600">Veri yüklenemedi.</div>}

                {!isLoading && !isError && (
                    <DataGrid
                        rows={kisiList}
                        columns={columns}
                        exportAllUrl="/api/v1/kisiler"
                        exportFileName="kisiler"
                        pagination={false}
                        className="h-[600px]"
                    />
                )}
                <div className="flex justify-end mt-4 space-x-2">
                    <Button onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0}>← Önceki</Button>
                    <span className="text-sm text-gray-600">Sayfa {page + 1}</span>
                    <Button onClick={() => setPage(p => p + 1)} disabled={kisiList.length < pageSize}>Sonraki →</Button>
                </div>
            </CardBody>
        </Card>
    )
}
