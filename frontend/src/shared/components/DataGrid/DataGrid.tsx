// shared/components/DataGrid/DataGrid.tsx
import {useRef, useState} from 'react'
import * as XLSX from 'xlsx'
import {
    ClientSideRowModelModule,
    ColDef,
    CustomFilterModule,
    DateFilterModule,
    ModuleRegistry,
    NumberFilterModule,
    PaginationModule,
    QuickFilterModule,
    TextFilterModule,
    ValidationModule
} from 'ag-grid-community'
import {AgGridReact} from 'ag-grid-react'
import classNames from 'classnames'

import 'ag-grid-community/styles/ag-theme-alpine.css'
import {api} from "@/shared/api/client.ts";

// Register necessary modules
ModuleRegistry.registerModules([
    ClientSideRowModelModule,
    ValidationModule,
    TextFilterModule,
    NumberFilterModule,
    DateFilterModule,
    CustomFilterModule,
    PaginationModule,
    QuickFilterModule,
])

export interface DataGridProps {
    rows: any[]
    columns: ColDef[]
    pagination?: boolean
    paginationPageSize?: number
    quickFilterText?: string
    exportAllFn?: () => Promise<any[]>
    exportAllUrl?: string
    exportFileName?: string
}

export function DataGrid({
                             rows,
                             columns,
                             pagination = true,
                             paginationPageSize = 10,
                             quickFilterText = '',
                             exportAllFn,
                             exportAllUrl,
                             exportFileName = 'data'
                         }: DataGridProps) {
    const gridRef = useRef<AgGridReact>(null)
    const [exportingAll, setExportingAll] = useState(false)

    // Utility: generate and download Excel
    const downloadExcel = (data: any[], sheetName: string, fileName: string) => {
        const ws = XLSX.utils.json_to_sheet(data)
        const wb = XLSX.utils.book_new()
        XLSX.utils.book_append_sheet(wb, ws, sheetName)
        XLSX.writeFile(wb, `${fileName}.xlsx`)
    }

    // Export current page data
    const handleExportPage = () => {
        downloadExcel(rows, 'PageData', `${exportFileName}_page`)
    }

    // Export full data via provided callback or URL paging loop using axios
    const handleExportAll = async () => {
        let allData: any[] = []
        try {
            setExportingAll(true)
            if (exportAllFn) {
                allData = await exportAllFn()
            } else if (exportAllUrl) {
                let skip = 0
                const limit = paginationPageSize
                while (true) {
                    const res = await api.get<any[]>(`${exportAllUrl}?skip=${skip}&limit=${limit}`)
                    const chunk = res.data
                    if (!chunk.length) break
                    allData = allData.concat(chunk)
                    skip += limit
                }
            } else {
                return
            }
            downloadExcel(allData, 'AllData', `${exportFileName}_all`)
        } finally {
            setExportingAll(false)
        }
    }

    return (
        <div className="flex flex-col space-y-2">
            {/* Export Buttons Toolbar */}
            <div className="flex space-x-2">
                {(exportAllFn || exportAllUrl) && (
                    <button
                        className="px-4 py-2 bg-blue-600 text-white rounded"
                        onClick={handleExportAll}
                        disabled={exportingAll}
                    >
                        {exportingAll ? 'Dışa Aktarılıyor...' : 'Tümünü Dışa Aktar'}
                    </button>
                )}
                <button
                    className="px-4 py-2 bg-gray-600 text-white rounded"
                    onClick={handleExportPage}
                >
                    Görüneni Dışa Aktar
                </button>
            </div>

            {/* AG Grid Container */}
            <div
                className={classNames(
                    'ag-theme-alpine shadow rounded-lg overflow-hidden'
                )}
                style={{width: '100%', height: 600}}
            >
                <AgGridReact
                    ref={gridRef}
                    rowModelType="clientSide"
                    rowData={rows}
                    columnDefs={columns}
                    defaultColDef={{sortable: true, filter: true, resizable: true}}
                    pagination={pagination}
                    paginationPageSize={paginationPageSize}
                    quickFilterText={quickFilterText}
                />
            </div>
        </div>
    )
}
