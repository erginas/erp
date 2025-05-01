// src/modules/kisiler/types/KisiTypes.ts

// Ana Kisi tipi (read işlemlerinde dönecek)
export interface Kisi {
    kimlik_no: number;
    adi: string;
    soyadi: string;
    baba_adi?: string;
    ana_adi?: string;
    meslegi?: string;
    dogum_yeri?: string;
    dogum_tarihi?: string; // ISO date string
    kan_grubu?: string;
    cinsiyeti?: "E" | "K";
    medeni_hali?: string;
    ev_tel?: string;
    cep_tel?: string;
    is_tel?: string;
    adres?: string;
    ssk_no?: string;
    ilgili_sirket?: string;
    ise_giris_tarihi?: string;
    isten_cikis_t?: string;
    vergi_dairesi?: string;
    vergi_no?: string;
    birim_no?: number;
    gorevi?: string;
    mesai_fl?: "N" | "C" | "M";
    aciklama?: string;
    aktif: number;
}

// Yeni Kisi oluşturma için gereken alanlar
export interface KisiCreate {
    kimlik_no: number;
    adi: string;
    soyadi: string;
    baba_adi?: string;
    ana_adi?: string;
    meslegi?: string;
    dogum_yeri?: string;
    dogum_tarihi?: string;
    kan_grubu?: string;
    cinsiyeti?: "E" | "K";
    medeni_hali?: string;
    ev_tel?: string;
    cep_tel?: string;
    is_tel?: string;
    adres?: string;
    ssk_no?: string;
    ilgili_sirket?: string;
    ise_giris_tarihi?: string;
    vergi_dairesi?: string;
    vergi_no?: string;
    birim_no?: number;
    gorevi?: string;
    mesai_fl?: "N" | "C" | "M";
    aciklama?: string;
}

// Kisi güncelleme için (partial)
export interface KisiUpdate {
    adi?: string;
    soyadi?: string;
    baba_adi?: string;
    ana_adi?: string;
    meslegi?: string;
    dogum_yeri?: string;
    dogum_tarihi?: string;
    kan_grubu?: string;
    cinsiyeti?: "E" | "K";
    medeni_hali?: string;
    ev_tel?: string;
    cep_tel?: string;
    is_tel?: string;
    adres?: string;
    ssk_no?: string;
    ilgili_sirket?: string;
    ise_giris_tarihi?: string;
    isten_cikis_t?: string;
    vergi_dairesi?: string;
    vergi_no?: string;
    birim_no?: number;
    gorevi?: string;
    mesai_fl?: "N" | "C" | "M";
    aciklama?: string;
    aktif?: number;
}

// Listeleme için public Kisi görünümü
export type KisiPublic = {
    kimlik_no: number;  // <<< Burayı string değil, number yapmalıyız ki kimlik_no integer çalışsın ✅
    adi: string;
    soyadi?: string | null;
}

// Liste response'u
export type KisilerPublic = {
    data: KisiPublic[];
    count: number;
}

// Backend başarılı işlem response'u (silme vb.)
export type Message = {
    message: string;
}

// --- API Request/Response Şemaları ---

// /kisiler/ → Listeleme
export type KisilerReadKisilerData = {
    limit?: number;
    skip?: number;
}

export type KisilerReadKisilerResponse = KisilerPublic;

// /kisiler/ → Yeni kayıt ekleme
export type KisilerCreateKisiData = {
    requestBody: KisiCreate;
}

export type KisilerCreateKisiResponse = KisiPublic;

// /kisiler/{kimlik_no} → Tek kayıt çekme
export type KisilerReadKisiData = {
    kimlik_no: number; // <<< Burayı da number yaptım ✅
}

export type KisilerReadKisiResponse = KisiPublic;

// /kisiler/{kimlik_no} → Güncelleme
export type KisilerUpdateKisiData = {
    kimlik_no: number;
    requestBody: KisiUpdate;
}

export type KisilerUpdateKisiResponse = KisiPublic;

// /kisiler/{kimlik_no} → Silme
export type KisilerDeleteKisiData = {
    kimlik_no: number;
}

export type KisilerDeleteKisiResponse = Message;
