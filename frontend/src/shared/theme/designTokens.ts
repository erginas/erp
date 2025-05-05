// shared/theme/designTokens.ts
// 🎨 Design tokens: renkler, boşluk, tipografi ve köşe yarıçapları

export const colors = {
    primary: '#2563EB',      // blue-600
    primaryDark: '#1D4ED8',  // blue-700
    secondary: '#64748B',    // slate-500
    background: '#F9FAFB',   // gray-50
    surface: '#FFFFFF',      // white
    text: '#111827',         // gray-900
    textSecondary: '#6B7280',// gray-500
    border: '#E5E7EB',       // gray-200
    error: '#DC2626',        // red-600
}

export const spacing = {
    xs: '4px',   // 0.25rem
    sm: '8px',   // 0.5rem
    md: '16px',  // 1rem
    lg: '24px',  // 1.5rem
    xl: '32px',  // 2rem
}

export const radii = {
    sm: '4px',   // rounded-sm
    md: '8px',   // rounded
    lg: '16px',  // rounded-lg
}

export const typography = {
    h1: {
        fontSize: '2rem',     // 32px
        lineHeight: '2.5rem', // 40px
        fontWeight: 700,
    },
    h2: {
        fontSize: '1.5rem',   // 24px
        lineHeight: '2rem',   // 32px
        fontWeight: 600,
    },
    body: {
        fontSize: '1rem',     // 16px
        lineHeight: '1.5rem', // 24px
        fontWeight: 400,
    },
    caption: {
        fontSize: '0.875rem', // 14px
        lineHeight: '1.25rem',// 20px
        fontWeight: 400,
    },
}
