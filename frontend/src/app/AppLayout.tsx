// src/app/AppLayout.tsx
import React from 'react'

export default function AppLayout({children}: { children: React.ReactNode }) {
    return (
        <div className="min-h-screen flex flex-col">
            {/* Sidebar, header vb. */}
            <main className="flex-1 p-4">
                {children}
            </main>
        </div>
    )
}