// features/hr/components/KisiForm.tsx
import React from 'react';
import { useForm } from 'react-hook-form';
import { Kisi, KisiCreate } from '../types/kisi';
import { Input } from '../../../shared/components/ui/Input';
import { Select } from '../../../shared/components/ui/select';
import { Button } from '../../../shared/components/ui/button';

interface Props {
  initialData?: Kisi;
  onSubmit: (data: KisiCreate) => void;
  onCancel: () => void;
}

export function KisiForm({ initialData, onSubmit, onCancel }: Props) {
  const { register, handleSubmit, reset } = useForm<KisiCreate>({
    defaultValues: initialData ? {
      ADI: initialData.ADI,
      SOYADI: initialData.SOYADI,
      CINSIYETI: initialData.CINSIYETI,
      MEDENI_HALI: initialData.MEDENI_HALI,
      EV_TEL: initialData.EV_TEL,
      CEP_TEL: initialData.CEP_TEL,
    } : undefined,
  });

  const submitHandler = (data: KisiCreate) => {
    onSubmit(data);
    reset();
  };

  return (
    <form onSubmit={handleSubmit(submitHandler)} className="space-y-4">
      <Input label="Adı" {...register('ADI')} />
      <Input label="Soyadı" {...register('SOYADI')} />
      <Select label="Cinsiyeti" {...register('CINSIYETI')} options={[{ value: 'E', label: 'Erkek' }, { value: 'K', label: 'Kadın' }]} />
      <Select label="Medeni Hali" {...register('MEDENI_HALI')} options={[{ value: 'Evli', label: 'Evli' }, { value: 'Bekar', label: 'Bekar' }]} />
      <Input label="Ev Telefonu" {...register('EV_TEL')} />
      <Input label="Cep Telefonu" {...register('CEP_TEL')} />
      <div className="flex justify-end space-x-2">
        <Button variant="secondary" onClick={onCancel}>İptal</Button>
        <Button type="submit">Kaydet</Button>
      </div>
    </form>
  );
}