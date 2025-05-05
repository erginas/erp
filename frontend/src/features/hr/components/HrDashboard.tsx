// features/hr/components/HrDashboard.tsx
// @ts-ignore
import React from 'react'

export function HrDashboard() {
    return (
        <div className="container mx-auto p-md">
            {/* Başlık */}
            <h1 className="text-h1 font-h1 text-primary mb-lg">
                İnsan Kaynakları Paneli
            </h1>

            {/* Kartlar */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-lg">
                {/* Toplam Çalışan Kartı */}
                <div className="bg-surface p-md rounded-md shadow">
                    <h2 className="text-h2 font-h2 text-textSecondary mb-sm">
                        Toplam Çalışan
                    </h2>
                    <p className="text-body font-body text-primary">350</p>
                </div>

                {/* Yeni Başvurular Kartı */}
                <div className="bg-surface p-md rounded-md shadow">
                    <h2 className="text-h2 font-h2 text-textSecondary mb-sm">
                        Yeni Başvurular
                    </h2>
                    <p className="text-body font-body text-primary">24</p>
                </div>

                {/* İzin Talepleri Kartı */}
                <div className="bg-surface p-md rounded-md shadow">
                    <h2 className="text-h2 font-h2 text-textSecondary mb-sm">
                        İzin Talepleri
                    </h2>
                    <p className="text-body font-body text-primary">8</p>
                </div>
            </div>
        </div>
    )
}
