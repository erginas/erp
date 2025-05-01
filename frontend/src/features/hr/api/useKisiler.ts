// features/hr/api/useKisiler.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../../../shared/api/client'
import type { Kisi, KisiCreate } from '../types/kisi'

export function useKisiler(skip = 0, limit = 100) {
  return useQuery<Kisi[]>({
    queryKey: ['kisiler', { skip, limit }],
    queryFn: () => api.get<Kisi[]>(`/api/v1/kisiler?skip=${skip}&limit=${limit}`)
                         .then(res => res.data),
    staleTime: 1000 * 60 * 5,
  })
}

export function useCreateKisi() {
  const qc = useQueryClient()
  return useMutation<Kisi, unknown, KisiCreate>({
    mutationFn: (data) => api.post<Kisi>('/api/v1/kisiler', data).then(res => res.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['kisiler'] }),
  })
}

export function useUpdateKisi() {
  const qc = useQueryClient()
  return useMutation<Kisi, unknown, Kisi>({
    mutationFn: (data) => api.put<Kisi>(`/api/v1/kisiler/${data.KIMLIK_NO}`, data)
                             .then(res => res.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['kisiler'] }),
  })
}

export function useDeleteKisi() {
  const qc = useQueryClient()
  return useMutation<void, unknown, string>({
    mutationFn: (key) => api.delete<void>(`/api/v1/kisiler/${key}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['kisiler'] }),
  })
}
