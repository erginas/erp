// src/modules/kisiler/types/KisiSchemas.ts

export const KisiCreateSchema = {
    type: "object",
    required: ["kimlik_no", "adi", "soyadi"],
    properties: {
        kimlik_no: {type: "integer", title: "Kimlik No"},
        adi: {type: "string", maxLength: 255, title: "Adı"},
        soyadi: {type: "string", maxLength: 255, title: "Soyadı"},
        baba_adi: {type: "string", maxLength: 255, nullable: true, title: "Baba Adı"},
        ana_adi: {type: "string", maxLength: 255, nullable: true, title: "Ana Adı"},
        meslegi: {type: "string", maxLength: 255, nullable: true, title: "Mesleği"},
        dogum_yeri: {type: "string", maxLength: 255, nullable: true, title: "Doğum Yeri"},
        dogum_tarihi: {type: "string", format: "date", nullable: true, title: "Doğum Tarihi"},
        kan_grubu: {type: "string", maxLength: 10, nullable: true, title: "Kan Grubu"},
        cinsiyeti: {type: "string", enum: ["E", "K"], title: "Cinsiyeti"},
        medeni_hali: {type: "string", maxLength: 10, nullable: true, title: "Medeni Hali"},
        ev_tel: {type: "string", maxLength: 50, nullable: true, title: "Ev Tel"},
        cep_tel: {type: "string", maxLength: 50, nullable: true, title: "Cep Tel"},
        is_tel: {type: "string", maxLength: 50, nullable: true, title: "İş Tel"},
        adres: {type: "string", maxLength: 1024, nullable: true, title: "Adres"},
        ssk_no: {type: "string", maxLength: 30, nullable: true, title: "SSK No"},
        ilgili_sirket: {type: "string", maxLength: 5, nullable: true, title: "İlgili Şirket"},
        ise_giris_tarihi: {type: "string", format: "date", nullable: true, title: "İşe Giriş Tarihi"},
        vergi_dairesi: {type: "string", maxLength: 120, nullable: true, title: "Vergi Dairesi"},
        vergi_no: {type: "string", maxLength: 20, nullable: true, title: "Vergi No"},
        birim_no: {type: "integer", nullable: true, title: "Birim No"},
        gorevi: {type: "string", maxLength: 80, nullable: true, title: "Görevi"},
        mesai_fl: {type: "string", enum: ["N", "C", "M"], title: "Mesai Durumu"},
        aciklama: {type: "string", maxLength: 1024, nullable: true, title: "Açıklama"},
        aktif: {type: "integer", title: "Aktif"},
    },
} as const;

export const KisiUpdateSchema = {
    type: "object",
    properties: {
        adi: {type: "string", maxLength: 255, nullable: true},
        soyadi: {type: "string", maxLength: 255, nullable: true},
        baba_adi: {type: "string", maxLength: 255, nullable: true},
        ana_adi: {type: "string", maxLength: 255, nullable: true},
        meslegi: {type: "string", maxLength: 255, nullable: true},
        dogum_yeri: {type: "string", maxLength: 255, nullable: true},
        dogum_tarihi: {type: "string", format: "date", nullable: true},
        kan_grubu: {type: "string", maxLength: 10, nullable: true},
        cinsiyeti: {type: "string", enum: ["E", "K"], nullable: true},
        medeni_hali: {type: "string", maxLength: 10, nullable: true},
        ev_tel: {type: "string", maxLength: 50, nullable: true},
        cep_tel: {type: "string", maxLength: 50, nullable: true},
        is_tel: {type: "string", maxLength: 50, nullable: true},
        adres: {type: "string", maxLength: 1024, nullable: true},
        ssk_no: {type: "string", maxLength: 30, nullable: true},
        ilgili_sirket: {type: "string", maxLength: 5, nullable: true},
        ise_giris_tarihi: {type: "string", format: "date", nullable: true},
        vergi_dairesi: {type: "string", maxLength: 120, nullable: true},
        vergi_no: {type: "string", maxLength: 20, nullable: true},
        birim_no: {type: "integer", nullable: true},
        gorevi: {type: "string", maxLength: 80, nullable: true},
        mesai_fl: {type: "string", enum: ["N", "C", "M"], nullable: true},
        aciklama: {type: "string", maxLength: 1024, nullable: true},
        aktif: {type: "integer", nullable: true},
    },
} as const;

export const KisiPublicSchema = {
    type: "object",
    required: ["kimlik_no", "adi", "soyadi"],
    properties: {
        kimlik_no: {type: "integer"},
        adi: {type: "string", maxLength: 255},
        soyadi: {type: "string", maxLength: 255},
    },
} as const;

export const KisisPublicSchema = {
    type: "object",
    required: ["data", "count"],
    properties: {
        data: {
            type: "array",
            items: {$ref: "#/components/schemas/KisiPublic"},
        },
        count: {type: "integer"},
    },
} as const;
