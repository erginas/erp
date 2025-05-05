// features/hr/api/useKisiler.ts
import {api} from '@/shared/api/client'
import {useQuery} from "@tanstack/react-query";
import {Kisi} from "@/features/hr/types/kisi.ts";

// Fetch total count (for fetchAll)
async function fetchKisiCount(): Promise<number> {
    const res = await api.get<{ count: number }>(`/api/v1/kisiler/count`)
    return res.data.count
}

interface UseKisilerOptions {
    page?: number       // zero-based page index
    pageSize?: number   // items per page
    fetchAll?: boolean  // if true, ignore pagination and fetch all
    search?: string     // e.g. "adi:Ahmet" or general term
}

export function useKisiler({
                               page = 0,
                               pageSize = 10,
                               fetchAll = false,
                               search,
                           }: UseKisilerOptions = {}) {
    return useQuery<Kisi[]>({
        queryKey: ['kisiler', page, pageSize, fetchAll, search],
        queryFn: async () => {
            let skip = page * pageSize
            let limit = pageSize

            // If fetchAll, override skip & limit
            if (fetchAll) {
                const total = await fetchKisiCount()
                skip = 0
                limit = total
            }

            // Build query params
            const params = new URLSearchParams()
            params.set('skip', String(skip))
            params.set('limit', String(limit))

            // Apply search filters
            if (search) {
                if (search.includes(':')) {
                    const [field, val] = search.split(':', 2)
                    params.set(field, val)
                } else {
                    params.set('search', search)
                }
            }

            const res = await api.get<Kisi[]>(`/api/v1/kisiler?${params.toString()}`)
            return res.data
        },
        staleTime: 1000 * 60 * 5,
        refetchOnWindowFocus: true,
    })
}
