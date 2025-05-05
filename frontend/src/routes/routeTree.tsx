// src/routes/routeTree.tsx
import React from 'react'
import {createRootRoute, createRoute, Outlet} from '@tanstack/react-router'
import AppLayout from '@/app/AppLayout'
import Dashboard from '@/features/dashboard/Dashboard'
import AdminPage from '@/features/auth/components/AdminPage'
import KisiListPage from '@/features/hr/pages/KisiListPage'
import LoginPage from "@/features/auth/components/LoginPage.tsx";
import RecoverPasswordPage from "@/features/auth/components/RecoverPasswordPage.tsx";
import ResetPasswordPage from "@/features/auth/components/ResetPasswordPage.tsx";
import SettingsPage from "@/features/auth/components/SettingsPage.tsx";
import {HrDashboard} from "@/features/hr/components/HrDashboard.tsx";


// 1️⃣ Root rotayı oluştur, 404 bileşeni ekle
export const rootRoute = createRootRoute({
    component: () => <Outlet/>,
    defaultNotFoundComponent: () => (
        <div className="flex h-screen items-center justify-center">
            <h1 className="text-3xl font-bold text-red-600">404 — Sayfa Bulunamadı</h1>
        </div>
    ),
})

// 2️⃣ Public/auth rotaları
const loginRoute = createRoute({
    path: '/login',
    getParentRoute: () => rootRoute,
    component: LoginPage,
})
const signupRoute = createRoute({
    path: '/signup',
    getParentRoute: () => rootRoute,
    // component: SignupPage,
})
const recoverPasswordRoute = createRoute({
    path: '/recover-password',
    getParentRoute: () => rootRoute,
    component: RecoverPasswordPage,
})
const resetPasswordRoute = createRoute({
    path: '/reset-password',
    getParentRoute: () => rootRoute,
    component: ResetPasswordPage,
})

// 3️⃣ Root’un çocuklarını ekle (mutlaka layoutRoute da burada olsun)
const layoutRoute = createRoute({
    path: '/',
    getParentRoute: () => rootRoute,
    component: AppLayout,
})
rootRoute.addChildren([
    loginRoute,
    signupRoute,
    recoverPasswordRoute,
    resetPasswordRoute,
    layoutRoute,   // ← burada ekliyoruz
])

// 4️⃣ Layout altı korumalı sayfalar

// 4a) Dashboard — **index** yolu: path: '' kullanıyoruz
const dashboardRoute = createRoute({
    path: '',                        // boş path = layoutRoute’un tam “/”'ü
    getParentRoute: () => layoutRoute,
    component: Dashboard,
})

// 4b) HR Dashboard ve altrota
const hrDashboardRoute = createRoute({
    path: 'dashboard',
    getParentRoute: () => layoutRoute,
    component: HrDashboard,
})
hrDashboardRoute.addChildren([
    createRoute({
        path: 'kisiler',
        getParentRoute: () => hrDashboardRoute,
        component: KisiListPage,
    }),
])

// 4c) Admin & Settings
const adminRoute = createRoute({
    path: 'admin',
    getParentRoute: () => layoutRoute,
    component: AdminPage,
})
const settingsRoute = createRoute({
    path: 'settings',
    getParentRoute: () => layoutRoute,
    component: SettingsPage,
})

// 5️⃣ layoutRoute’e çocukları ekle
layoutRoute.addChildren([
    dashboardRoute,
    hrDashboardRoute,
    adminRoute,
    settingsRoute,
])

// 6️⃣ En dışa verdiğimiz ağaç
export const routeTree = rootRoute