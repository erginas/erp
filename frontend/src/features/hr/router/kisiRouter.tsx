// src/modules/kisiler/router/kisiRouter.tsx
// @ts-ignore
import React from "react";
import {Container, Heading} from "@chakra-ui/react";
import {createRoute} from "@tanstack/react-router";
import {z} from "zod";

import {layoutRoute} from "@/app/_layout.tsx";
import AddKisi from "../components/AddKisi.tsx";
import KisilerTable from "@/features/kisiler/components/KisilerTable.tsx";

// 1️⃣ Query string validasyonu için Zod şeması
const kisiSearchSchema = z.object({
    page: z.number().catch(1),  // page parametresi yoksa veya hatalıysa 1 olsun
});

// 2️⃣ Route tanımı
export const kisilerRoute = createRoute({
    path: "/kisiler",
    getParentRoute: () => layoutRoute,
    component: KisilerPage,
    validateSearch: (search) => kisiSearchSchema.parse(search),
});

function KisilerPage() {
    return (
        <Container maxW="full" p={4}>
            <Heading size="lg" pt={12}>
                Kişiler Yönetimi
            </Heading>
            <AddKisi/>
            {/*<KisiList/>*/}
            <KisilerTable/>
        </Container>
    );
}
