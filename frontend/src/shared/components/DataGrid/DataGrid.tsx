// shared/components/DataGrid/DataGrid.tsx
// @ts-ignore
import React from 'react';
import {ClientSideRowModelModule, ModuleRegistry, ValidationModule} from 'ag-grid-community';
// import { ClientSideRowModelModule } from 'ag-grid-community/client-side-row-model';
// import { ValidationModule }       from 'ag-grid-community/validation';
import { AgGridReact }           from 'ag-grid-react';
import { ColDef }                from 'ag-grid-community';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';

// Modülleri kaydet (sadece bir kez)
ModuleRegistry.registerModules([
  ClientSideRowModelModule,
  ValidationModule,
]);

interface DataGridProps {
  rows: any[];
  columns: ColDef[];
}

export function DataGrid({ rows, columns }: DataGridProps) {
  return (
    <div className="ag-theme-alpine" style={{ width: '100%', height: 500 }}>
      <AgGridReact
        rowData={rows}
        columnDefs={columns}
        defaultColDef={{ sortable: true, filter: true, resizable: true }}
      />
    </div>
  );
}
