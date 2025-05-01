// features/hr/types/kisi.ts
export interface Kisi {
  KIMLIK_NO: string;
  ADI: string;
  SOYADI: string;
  BABA_ADI: string;
  ANA_ADI: string;
  MESLEGI: string;
  DOGUM_YERI: string;
  KAN_GRUBU: string;
  CINSIYETI: string;
  MEDENI_HALI: string;
  EV_TEL?: string;
  CEP_TEL?: string;
  IS_TEL?: string;
  ADRES: string;
  ILGILI_SIRKET: string;
  ISTEN_CIKIS_T?: string;
  GOREVI: string;
  MESAI_FL: boolean;
  EGITIM_DURUMU: string;
  DOGUM_AY?: number;
  DOGUM_YIL?: number;
  ORG_ADI?: string;
  GOREV_ADI?: string;
  SSK_NO?: string;
  ISE_GIRIS_TARIHI?: string;
}
export type KisiCreate = Omit<Kisi, 'KIMLIK_NO'>;